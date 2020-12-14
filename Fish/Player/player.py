from Common.state import State
from Common.game_tree import GameTreeNode
from Player.strategy import Strategy
from Common.player_interface import Player_Interface
import uuid
import json
from multiprocessing import Queue

# TODO: Refactor to allow for an arbitrary strategy to be used

# TODO: Add way of caching and updating local game tree when moves are taken

class PlayerAI(Player_Interface):
    """
    Implementation of player_interface for a simple player AI based off of the strategy located within strategy.py.
    All player AI given to the referee must extend player_interface.
    """

    def __init__(self, strategy: Strategy, name=None):
        """
            __init__ - Creates a Player AI when given the turn index of the player, and the state of the Board.
            Parameters:
            Mandatory:
                turn_idx - Integer representing when this players turn is in the state.
                state - the current State of the board.


            Optional:
                depth - The depth of the minmax search for the PlayerAI

            Output -> A PlayerAI with the given turn index, board, and depth of search.
        """
        if name is None:
            name = "default"  # TODO: Make this unique
        self.name = name
        self.state = None
        self.turn_idx = 0
        self.strategy = strategy
        self.id = uuid.uuid1()

    def get_placement(self):
        """
            get_placement - Returns this players next placement given the current state of the board.

            Output -> a List containing a single tuple (x,y) representing the x and y coordinates of this players next placement given the current state of the board.

        """
        return self.strategy.get_placement(self.state)

    def get_next_move(self, actions: list):
        """
            get_next_move - Returns this players next move given the current state of the board.

            Output -> a List containing two tuples [(x1,y1),(x2,y2)] where x1 and y1 represent the x and y coordinates of the penguin the player wants to move.
                and x2 and y2 represent the coordinates of the space the player would like to move the penguin to.
        """
        return self.strategy.get_move(self.state, actions)

    def set_turn_idx(self, turn_idx):
        self.turn_idx = turn_idx

    def update_state(self, state: State):
        """
            update_state - Updates the gamestate this player runs off of.  This function is used by the referee to give the player updated gamestates.
        """
        self.state = state

    def get_turn_idx(self):
        """
            get_turn_idx - Returns the turn index of this players

            Output -> An integer representing the turn index of this player.
        """
        return self.turn_idx

    def decrement_turn_idx(self):
        """
            decrement_turn_idx - Decrements the turn index of this player.  This function is used when a player is removed from the game by the referee.
        """
        self.turn_idx = self.turn_idx - 1

    def get_state(self):
        """
            get_state - returns the state that this playerAI is currently using.

            Output -> A State representing this players current gamestate.
        """
        return State.from_state(self.state)

    def __str__(self):
        player_dict = {
            'turn_idx': self.turn_idx,
            'state': str(self.state),
            'depth': self.depth
        }
        return json.dumps(player_dict)

    def inform_end(self, is_winner: bool):
        return self.strategy.end(is_winner)

    def inform_start(self):
        return self.strategy.start()

    def inform_color(self, color: str):
        return self.strategy.set_color(color)

    def inform_opponents(self, colors: list):
        return self.strategy.set_other_players(colors)

    def inform_remove(self):
        self.strategy.kill_client()

    def __eq__(self, other):
        """
        __eq__ - Checks for Equaility between two playerAIs that are not savedas the same object

        Output -> True if the given PlayerAI has the same state and depth as this one, False otherwise
        """
        return isinstance(other, PlayerAI) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
