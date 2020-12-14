from Common.board import Board
from tkinter import *
from Common.player import Player
from Common.utils import parse_json
import json
from copy import deepcopy
from enum import Enum


class Game_Phase(Enum):
    PLACEMENT = 0
    PLAYING = 1
    GAME_OVER = 2

"""
Data representation for the game state. An instance of State contains a Board object representing the tiles on the game
board, a list of Player objects containing score/color/player penguin locations, and a turn index indicating which player
is currently taking an action.  Penguin locations for each player are stored within the player object for each player.
The order of players is stored based off the order of the list of players, combined with the turn_index, which points to the location
within the list of the player with the current turn.
"""
class State:
    """
    __init__: Constructs a State from the provided list of players, tiles, and player_order

    Params:
        players: list - A list of dictionaries, where each dictionary in the list represents a Player object. A valid
                        dictionary input would contain a 'color' (str), 'score' (int), and 'places' (list of tuples)
                        fields.
                        A valid dictionary would be something like:
                        {
                            "color": "blue",
                            "score": 0,
                            "places": [[0, 0], [1, 1]]
                        }
                        color represents the player color, score represents the player score, and places represents the
                        coordinates at which the player has penguins on the board.
        tiles: list - A list of list of integers representing the board texture. A value of 0 indicates that the tile is
                      a hole
        turn_index: (optional) - An optional integer representing the index of the player that is currently performing
                                 an action.
    """
    def __init__(self, players: list, tiles: list, turn_index = 0, game_phase = Game_Phase.PLACEMENT):
        self.board = Board.make_board_from_tiles(tiles)
        self.players = []
        self.turn_index = turn_index
        for player in players:
            ##TODO: Should we check whether the penguins are non overlapping and at valid Tile coordinates?
            self.players.append(Player.dictToPlayer(player))
        self.game_phase = game_phase
        self.set_penguins()

    """
    from_state: static constructor that takes in a state and returns a deep copy of that state.

    Params:
        state: State - The state that will be deep copied

    Output -> State that is identical to the provided state
    """
    @staticmethod
    def from_state(state: 'State'):
        tiles = state.get_board_tiles()
        players = state.get_players(toDict=True)
        turn_index = state.get_turn_idx()
        phase = state.get_game_phase()
        return State(players, tiles, turn_index=turn_index, game_phase=phase)

    def set_penguins(self):
        for player in self.players:
            for penguin_posn in player.get_penguin_locations():
                if self.board.check_valid_tile(penguin_posn[0], penguin_posn[1]):
                    self.board.place_player(penguin_posn)
                else:
                    raise ValueError("Invalid penguin placement")

    """
    place_penguin: Places a penguin for the specified player at the specified location (row/column coord). If the tile
                   is a Player tile (already occupied by another player penguin), then place_penguin throws an error.

    Params:
        player_color: str - String containing a color that is associated with the player

        Output -> State that is identical to the provided state
        """
    def place_penguin(self, location: tuple):
        if self.valid_placement(location):
            self.players[self.get_turn_idx()].add_penguin(location)
            self.board.place_player(location)
            self.transition()
        else:
            raise ValueError("Unable to place penguin because the specified tile is not valid or the player has 6 penguins")

    def move_penguin(self, origin: tuple, destination: tuple):

        player = self.players[self.get_turn_idx()]

        if origin not in player.get_penguin_locations():
            raise ValueError("The specified player does not have a penguin in the provided origin coordinates")
        elif not self.valid_move(origin, destination):
            raise ValueError("Unable to place penguin because the specified move is not valid")
        else:
            self.players[self.get_turn_idx()].move_penguin(origin, destination)
            self.players[self.get_turn_idx()].add_score(self.board.board[origin[0]][origin[1]].get_fish())
            self.board.remove_tile(origin[0], origin[1])
            self.board.place_player(destination)
            self.transition()

    def remove_player(self, turn_idx: int):
        for penguin in self.players[turn_idx].get_penguin_locations():
            self.remove_penguin(penguin, turn_idx)
        self.players.pop(turn_idx)
        if turn_idx == len(self.players) - 1:
            self.turn_index = 0

    def remove_penguin(self, origin: tuple, turn_idx: int):
        if origin not in self.players[turn_idx].get_penguin_locations():
            raise ValueError("The specified player does not have a penguin in the provided origin coordinates")
        else:
            self.players[turn_idx].remove_penguin(origin)
            self.board.remove_penguin(origin)


    def transition(self):
        if self.game_phase == Game_Phase.PLACEMENT:
            if self.placement_over():
                self.game_phase = Game_Phase.PLAYING
                self.turn_index = 0
            else:
                self.turn_index = (self.turn_index + 1) % len(self.players)
        elif self.game_phase == Game_Phase.PLAYING:
            if self.game_over():
                self.turn_index = -1
                self.game_phase = Game_Phase.GAME_OVER
                return
            else:
                self.turn_index = (self.turn_index + 1) % len(self.players)
                if not self.can_player_move(self.turn_index):
                    for i in range(self.turn_index, self.turn_index + len(self.players)):
                        if self.can_player_move(i % len(self.players)):
                            self.turn_index = i % len(self.players)
                            return
                        else:
                            self.turn_index = i % len(self.players)
                    self.game_phase == Game_Phase.GAME_OVER

    def valid_move(self, origin: tuple, destination: tuple):
        if self.game_phase != Game_Phase.PLAYING:
            raise ValueError("The game is not currently accepting movement of avatars")
        if origin not in self.players[self.turn_index].get_penguin_locations():
            return False
        return destination in self.board.reachable_spaces(origin[0], origin[1])

    def valid_placement(self, location: tuple):
        if self.game_phase != Game_Phase.PLACEMENT:
            return False
        player = self.players[self.get_turn_idx()]
        if not self.board.check_valid_tile(location[0], location[1]) or len(player.get_penguin_locations()) >= 6 - len(self.players):
            return False
        return True

    def get_valid_moves_from_penguin(self, origin: tuple):
        moves = []
        for destination in self.board.reachable_spaces(origin[0], origin[1]):
            moves.append([(origin[0], origin[1]), (destination[0], destination[1])])
        return moves

    def get_valid_moves(self):
        moves = []
        player = self.players[self.turn_index]
        for penguin in player.get_penguin_locations():
            moves.extend(self.get_valid_moves_from_penguin((penguin[0], penguin[1])))
        return moves

    def get_player_index(self, player_color: str):
        for i in range(len(self.players)):
            if self.players[i].get_color() == player_color:
                return i
        return -1

    def game_over(self):
        for i in range(len(self.players)):
            if self.can_player_move(i):
                return False
        return True

    def placement_over(self):
        for player in self.players:
            if len(player.get_penguin_locations()) < 6 - len(self.players):
                return False
        return True

    def can_player_move(self, idx: int):
        for penguin_posn in self.players[idx].get_penguin_locations():
            if len(self.board.reachable_spaces(penguin_posn[0], penguin_posn[1])) != 0:
                return True
        return False

    def draw(self, window, size):
        self.board.draw(window, size)
        self.draw_players(window, size)

    def draw_players(self, window, size):
        player_size = size * .25
        tile_origin = lambda x: (x[0], (4 * x[1]) + 3) if x[0] % 2 == 0 else (x[0], (4 * x[1]) + 1)

        for player in self.players:
            for penguin_posn in player.get_penguin_locations():
                print(penguin_posn)
                origin = [coord * size for coord in tile_origin(penguin_posn)]
                x_coord = 2 * size + origin[1]
                y_coord = 1 * size + origin[0]
                window.create_rectangle(x_coord - (player_size / 2), y_coord - (player_size / 2), x_coord + (player_size / 2), y_coord + (player_size / 2), fill=player.get_color())
            


        
        
        
        
                # window.create_polygon(x_coord, y_coord,
                #                       x_coord + size, y_coord,
                #                       x_coord + size, y_coord + size,
                #                       x_coord, y_coord + size,
                #                       fill=player.get_color(),
                #                       outline="black")  # Fill white
#
#     def get_valid_moves(self, player_color: str, penguin_posn: tuple):
#         player = self.players[player_color]
#         if penguin_posn not in player.get_penguin_locations():
#             return []
#         return self.board.movable_spaces(penguin_posn[0], penguin_posn[1], self.players)
#
    def get_board_tiles(self):
        return self.board.get_board()

    def get_players(self, toDict = False):
        players = []
        for player in self.players:
            new_player = Player.fromPlayer(player)
            if toDict:
                new_player = new_player.toDict()
            players.append(new_player)
        return players

    def get_players_in_order(self):
        players_list = [player.toDict() for player in self.get_players()]
        for i in range(0, self.get_turn_idx()):
            players_list = players_list[1:] + [players_list[0]]
        #This does not correctly rotate the list:
        #players_list[self.get_turn_idx():].extend(players_list[0:self.get_turn_idx()])
        return players_list

    def get_turn_idx(self):
        return self.turn_index

    #Returns a formatted dictionary for integration tests
    #prepare_json: -> State (Dictionary)
    def prepare_json(self):
        ret = {
            'players': self.get_players_in_order(),
            'board': self.get_board_tiles()
        }
        return ret

    def get_game_phase(self):
        return self.game_phase

    def get_player_color(self):
        self.players[self.turn_index].get_color()

    def get_board_size(self):
        return self.board.get_board_size()

    def __str__(self):
        players_list = [player.toDict() for player in self.get_players()]
        players_list[self.get_turn_idx():].extend(players_list[0:self.get_turn_idx()])
        dict = {
            'players': players_list,
            'board': self.get_board_tiles()
        }
        return json.dumps(dict)
    
    def render_state(self):
        window = Tk()
        draw = Canvas(window, width=50 * 5, height=50 * 4)
        window.geometry("500x500")
        self.draw(draw, 150)

        draw.pack(fill = BOTH, expand = True)
        window.mainloop()

    def __eq__(self, other):
        if not isinstance(other, State):
            return NotImplemented
        return self.get_board_tiles() == other.get_board_tiles() \
               and self.get_players(toDict=True) == other.get_players(toDict=True) \
               and self.get_turn_idx() == other.get_turn_idx()

# if __name__ == "__main__":
#     raw_data = sys.stdin.read()
#     input = list(parse_json(raw_data))
#     if len(input) > 1:
#         raise ValueError("Invalid game state")
#     input = input[0]
#     players = input['players']
#     board = input['board']
#     print(players)
#     print(board)
#     game = State(players, tiles=board)
#
#     window = Tk()
#     draw = Canvas(window, width=50 * 5, height=50 * 4)
#     window.geometry("500x500")
#     game.draw(draw, 50)
#     draw.pack(fill = BOTH, expand = True)
#     window.mainloop()
