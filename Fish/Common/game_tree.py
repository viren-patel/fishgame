from Common.state import State, Game_Phase
from Common.player import Player
from copy import deepcopy
"""
Data representation for a game tree representing the tree of all possible states from a starting state.
Each node in the game tree contains a State, a list indicating the order of the players, a reference
to the parent GameTreeNode, and a list of all direct children, or successor states given the current state.
A tree can be generated using a GameTreeNode using the generate_tree method, which will generate the tree up to the depth
you specify.
The game tree node can represent two of nodes:
    - game-is-over
    - current-player-can-move
The last state, current-player-is-stuck, cannot be represented by our state because our state automatically updates the
turn index to the next player that has any valid moves remaining, therefore eliminating that possibility.
"""
class GameTreeNode():
    # TODO: Refactor GameTree to be more... functional
    """
        __init__ - Creates a GameTreeNode given either the players, tiles, and parent, or given a State and parent.
        Parameters:
        Mandatory
            Either:
                players - List of Player objects, in order of turn.
                tiles - List of tiles representing the full structure of the board. Tile should be represented in a MxN list of list of ints, where
                        each int represents the number of fish on the tile.
            Or:
                state - A complete State. This state will be used as the starting state for this node.
    """


class GameTreeNode:
    """
    Data representation for a game tree representing the tree of all possible states from a starting state.
    Each node in the game tree contains a State, a list indicating the order of the players, a reference
    to the parent GameTreeNode, and a list of all direct children, or successor states given the current state.
    A tree can be generated using a GameTreeNode using the generate_tree method, which will generate the tree up to the depth
    you specify.
    The game tree node can represent two of nodes:
        - game-is-over
        - current-player-can-move
    The last state, current-player-is-stuck, cannot be represented by our state because our state automatically updates the
    turn index to the next player that has any valid moves remaining, therefore eliminating that possibility.
    """

    def __init__(self, state: State, moves = []):
        """
            __init__ - Creates a GameTreeNode given either the players, tiles, and parent, or given a State and parent.
            Parameters:
            Mandatory
                Either:
                    players - List of Player objects, in order of turn.
                    tiles - List of tiles representing the full structure of the board. Tile should be represented in a MxN list of list of ints, where
                            each int represents the number of fish on the tile.
                Or:
                    state - A complete State. This state will be used as the starting state for this node.

            Optional:
                parent - The parent node of this GameTreeNode.

            Output -> A Tree_node object with the provided players, tiles, and parent.
            """
        self.state = State.from_state(state)
        self.previous_moves = moves
        # TODO: children should be a dict to make finding pregenerated children easier
        self.children = []

    def check_valid_move(self, penguin_posn: tuple, destination: int):
        """
        check_valid_move - Checks whether the given move is legal. Returns a boolean.
        Parameters:
            player_color - color of player
            penguin_posn - position (in tuple) of penguin to be moved
            destination - position (in tuple) of destination coordinates
        Output -> True if the move is valid, else False
        """
        return self.state.valid_move(penguin_posn, destination)

    def check_available_actions(self):
        """
        check_available_moves - Gets game states of all possible moves from the current state and player penguin.
        Parameters:
        player_color - color of player
        penguin_posn - position (in tuple) of penguin to be moved
        Output -> List of valid successor states given the current state, current player's turn, and penguin that will be moved.
        """
        return self.state.get_valid_moves()

    def generate_tree(self, depth=1):
        """
        def generate_tree - Generates a tree of nodes to the depth that is given.  The default depth of the tree is 1.  Successors are stored in this nodes
            list of children.
        Parameters:
            depth - an integer representing the depth of the tree to be created.  A depth of 1 generates direct successors of this node.
        """
        if depth > 0 and not self.state.game_over():
            states = self.check_available_moves()
            for state in states:
                child = GameTreeNode(state=state, parent=self)
                self.children.append(child)
            for child in self.children:
                child.generate_tree(depth=depth-1)

    def generate_successor(self, action: list):
        """
        generate_successor - Query function that takes in a GameTreeNode, penguin position, and destination coordinates
                        and either signals that the action is illegal by returning None or returns the resulting state from the action.
        Parameters:
            action: list - An action is one of:
                            - A list containing one tuple [(row, col)]. This represents a placement.
                            - A list containing 2 tuples [(origin-row, origin-col), (dest-row, dest-col)], representing a
                              movement.
        """
        state = State.from_state(self.state)
        try:
            if len(action) == 0:
                return state
            if self.state.get_game_phase() == Game_Phase.PLACEMENT:
                state.place_penguin(action[0])
            elif self.state.get_game_phase() == Game_Phase.PLAYING:
                state.move_penguin(action[0], action[1])
            else:
                raise ValueError("")
            return state
        except (ValueError, IndexError):
            return None

    def get_game_state(self):
        return {"Board" : self.state.get_board(),
                "Scores" : self.state.get_scores(),
                "Players" : self.state.get_players(),
                "Turns" : self.state.turn_order()}

    def get_state(self):
        return State.from_state(self.state)

    def map_game_states(self, node, function):
        """
        map_game_states - Static query method that takes a GameTreeNode and applies the given function over all game states that are
                          directly reachable from the state in the provided GameTreeNode in 1 action.
        """
        player = self.state.get_current_player()
        states = []
        for penguin_posn in player.get_penguin_locations():
            states.extend(self.check_available_moves(player.get_color(), penguin_posn))
        result = []
        for state in states:
            result.append(function(state))
        return result
