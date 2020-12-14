import sys
sys.path.insert(1, '../Fish')
from Admin.manager import Tournament
from Common.state import State
from Player.player import PlayerAI
from Player.strategy import RemoteStrategy
from Common.utils import parse_json
import socket
import threading
import json
import multiprocessing
import time

VOID_MSG = "void"
MIN_TOURNAMENT_SIZE = 5
MAX_TOURNAMENT_SIZE = 10
NUM_WAIT_RETRIES = 2
DEBUGGING = False


def is_posn(posn):
    """Returns True if the given posn is a valid Position.

       output: bool 
    """
    return len(posn) == 2 and isinstance(posn[0], int) and isinstance(posn[1], int)


def is_move(move):
    """Returns True if the given input is a valid Move.

       output: bool
    """
    return len(move) == 2 and is_posn(move[0]) and is_posn(move[1])


def check_valid_response(data, func):
    """Returns True if the given data is not None and if the given function returns True when given the data:

    Parameters:

    data: Any - the data to be checked

    func: [Any -> bool] - a function used to check the validity of the data

    Output: bool
    """
    return data and func(data)


def is_void_msg(msg):
    """Returns True if the given msg is a valid void message.

    Parameters:

    msg: the message to be checked

    Output: bool
    """
    return msg == VOID_MSG

class FishClient:
    """
    Serves as a server-side representation of a client and handles interactions with the client.
    """

    def __init__(self, client_socket, addr):
        self.closed = False
        self.client_socket = client_socket
        self.addr = addr
        self.name = None

    def set_name(self, name):
        """
        Sets the name associated with this client.
        """
        self.name = name

    def get_player_name(self):
        """
        Gets the player name from the client. Returns None if no valid name is received or the request times out after ten seconds.
        """
        old_timeout = self.client_socket.gettimeout()
        try:
            self.client_socket.settimeout(10)
            response = self.receive_from_client()
        except socket.timeout:
            response = None
        self.client_socket.settimeout(old_timeout)
        return response if check_valid_response(response, lambda x: 0 < len(x) <= 12 and x.isalpha()) else None

    def start(self):
        """
        Sends a message to the client indicating the tournament has begun. Returns True if VOID_MSG is returned, False if an invalid string is received.
        """
        self.send_method_call("start", True)
        response = self.receive_from_client()
        return check_valid_response(response, is_void_msg)

    def setup(self, state):
        """Requests a placement from the client for the given State. Returns the position where the client would like to place
           their penguin. Returns None if the data sent back was malformed.
        """
        state_json = state.prepare_json()
        self.send_method_call("setup", state_json)

        response = self.receive_from_client()
        return response if check_valid_response(response, is_posn) else None

    def take_turn(self, state, actions: list):
        """Requests a Move from the client for the given State and supplies the actions that have taken place
           since their last turn. Returns the Move sent back by the client or None if the data sent back was malformed.

           output: Move
        """
        state_json = state.prepare_json()
        self.send_method_call("take-turn", state_json, actions)
        response = self.receive_from_client()
        return response if check_valid_response(response, is_move) else None

    def playing_as(self, color: str):
        """Notifies the client of the color they are playing as in their current game. Returns True if the player correctly
           responded with a void message.

           output: bool
        """
        self.send_method_call("playing-as", color)
        response = self.receive_from_client()
        return check_valid_response(response, is_void_msg)

    def playing_with(self, colors: list):
        """Notifies the client of the colors of the other players in their current game. Returns True if the player correctly
           responded with a void message.

           output: bool
        """
        self.send_method_call("playing-with", colors)
        response = self.receive_from_client()
        return check_valid_response(response, is_void_msg)

    def end(self, is_winner):
        """Notifies the client of tournament end and whether or not they are a winner. Returns True if the player correctly
           responded with a void message.

           output: bool
        """
        self.send_method_call("end", is_winner)
        response = self.receive_from_client()
        return check_valid_response(response, is_void_msg)

    def receive_from_client(self):
        """Receives JSON data from the client and serializes it

        output: JSON
        """
        if self.closed:
            return None
        receiving = True
        data = ''
        new_data = self.client_socket.recv(4096).decode()
        if new_data:
            print("Data received: {}".format(new_data)) if DEBUGGING else None
            data += new_data
        else:
            receiving = False
        try:
            ret = parse_json(data)
        except ValueError:
            ret = None
        print("RECEIVED: ", ret) if DEBUGGING else None
        return ret

    def send_method_call(self, func, *args):
        """Sends a method call to the client with the given function name and the given arguments
        """
        if self.closed:
            return
        msg = [func, args]
        print("SENDING", msg) if DEBUGGING else None
        self.client_socket.sendall(json.dumps(msg).encode())

    def end_connection(self):
        """Closes the connection to the client
        """
        self.closed = True
        self.client_socket.close()


class FishServer:

    def __init__(self):
        self.socket = None
        self.tournament = None
        self.clients = []

    def run_server(self, port: int) -> None:
        """
        Runs a tournament server until the tournament is completed.

        :param port: The port on which the server is to be hosted.
        :return: None
        """
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = soc
        soc.bind(('', port))
        soc.listen()

        # while len(threads) < min game size
        if not self.accept_new_connections():
            print("Not enough players for a tourney, shutting down") if DEBUGGING else None
            self.cancel_early()
            return

        # TODO: This should be multithreaded and should start from when the client connections, not when the waiting period is over
        for client in self.clients:
            print("Getting name of client...") if DEBUGGING else None
            name = client.get_player_name()
            if name is None:
                self.remove_client(client)
                print("Client timed out!") if DEBUGGING else None
            else:
                client.set_name(name)
                print("Received client name '{}'".format(name)) if DEBUGGING else None
        if len(self.clients) < MIN_TOURNAMENT_SIZE:
            self.cancel_early()
            print("Too many clients failed to respond with a name, ending tournament") if DEBUGGING else None
            return
        tournament = self.construct_tournament()
        print("Running tournament with {} players!".format(len(self.clients))) if DEBUGGING else None
        tournament.run_tournament()

        # tournament logic here

        soc.close()  # this happens after the tournament is over
        return self.get_tournament_result(tournament)

    def cancel_early(self):
        for client in self.clients:
            client.end_connection()
        self.socket.close()

    def remove_client(self, client):
        client.end_connection()
        self.clients.remove(client)

    def construct_tournament(self):
        """Constructs a Tournament object using the remote Players that have connected to the server.

        Output: Tournament
        """
        players = [PlayerAI(RemoteStrategy(fish_client), name=fish_client.name) for fish_client in self.clients]
        return Tournament(players)

    def get_tournament_result(self, tournament):
        """Returns a list of the form [w, cf] where w is the number of winning players and cf is the number of cheating or failed players.

        Parameters:

        tournament: Tournament - The Tournament Manager to get the number of winners and cheaters / losers

        Output: a list specified above
        """
        return [len(tournament.remaining_players), len(tournament.cheating_players) + len(tournament.failed_players)]


    def accept_new_connections(self) -> bool:
        """
        Accepts new connections until ten seconds have elapsed from the last waiting period and a game is able to start.

        :param soc: The open socket through which new connections should be accepted.
        :param threads: A list of active threads.
        :return: None
        """
        timer = 0.0
        self.socket.settimeout(1)
        for i in range(NUM_WAIT_RETRIES):
            print("Waiting room period {}".format(i)) if DEBUGGING else None
            while timer <= 30 and len(self.clients) < MAX_TOURNAMENT_SIZE:
                start_time = time.time()
                try:
                    client_soc, addr = self.socket.accept()
                    print("New client with address {} accepted".format(addr)) if DEBUGGING else None
                    new_client = FishClient(client_soc, addr)
                    self.clients.append(new_client)
                except socket.timeout:
                    print("Timed out within waiting room, waiting another second") if DEBUGGING else None
                timer += time.time() - start_time
            if len(self.clients) >= MIN_TOURNAMENT_SIZE:
                return True
        return False