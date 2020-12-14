import abc

from Common.game_tree import GameTreeNode
from Common.state import State, Game_Phase

# TODO: Make an abstract strategy class and make two implementations:
#  - MinimaxStrategy
#  - RemoteStrategy


class Strategy(abc.ABC):
    """ Returns a placement according to this Strategy for the given State

        Params:
            state: State - the current gamestate
        
        Output:
            Position
    """
    @abc.abstractmethod
    def get_placement(self, state: State):
        pass

    """ Returns a movement according to this Strategy for the given State

        Params:
            state: State - the current gamestate

        Output:
            Move
    """
    @abc.abstractmethod
    def get_move(self, state: State, actions: list):
        pass

    @abc.abstractmethod
    def set_color(self, color: str):
        pass

    @abc.abstractmethod
    def set_other_players(self, colors: list):
        pass

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def end(self, is_winner):
        pass

    @abc.abstractmethod
    def kill_client(self):
        pass


class MinimaxStrategy(Strategy):

    def __init__(self, depth):
        if depth < 1:
            raise ValueError("Invalid depth for Minimax Strategy")
        else:
            self.depth = depth

    def get_placement(self, state: State):
        return self.place_penguin(state)

    def get_move(self, state: State, actions: list):
        return self.get_optimal_action(GameTreeNode(state))

    def place_penguin(self, state: State):
        """
        place_penguins: Takes a State and modifies the state in place to automatically place player penguins on
                            the board until each player has 6-N penguins. This method starts from the top left
                            corner (0, 0) and goes from left to right until each row is filled up, at which point it will
                            move down a row. This method assumes that the board contained
                            in the game state is large enough to accommodate all penguins.

        Params:
            state: State - The provided state.
        """
        if not state:
            return None
        rows, columns = state.get_board_size()
        for i in range(rows):
            for j in range(columns):
                if state.valid_placement((i, j)):
                    return [(i, j)]
        return None

    def get_optimal_action(self, node: GameTreeNode):
        # TODO: Make this actually use node.generate_tree() so it caches data!
        """
        get_optimal_action: Runs a minimax search on the provided GameTreeNode to the provided depth "d to determine the move
                            with the optimal "reward" (player score) for the current player after D moves, assuming that all
                            other players will play with the intent to minimize the current player's score. This function
                            takes in a GameTreeNode and evaluates the "reward" for each available action with a recursive
                            minimax evaluation function. This method returns an Action, which is a list of tuples in the
                            form [(w, x), (y, z)], where the first pair of coordinates represents the current position of
                            the penguin and the second pair of coordinates represents the intended destination.
                            In the case of a tiebreaker, a tiebreaker method gets called that will prioritize by origin
                            row coord, origin column coord, destination row coord, and destination column coord in that order.
        Params:
            node: GameTreeNode - The initial node, to which no more players will be added. This node should contain a state with
                                game phase PLAYING.

        Output -> A list of tuples in the form [(a, b), (c, d)] representing the optimal action. (a, b) represents the origin
                and (c, d) represents the destination. If the game is over, then this method returns None.
        """
        
        if not node or node.get_state().game_over():
            return None
        max_score = float("-inf")
        optimal_actions = []
        idx = node.get_state().get_turn_idx()
        for action in node.check_available_actions():
            successor_state = node.generate_successor(action)
            successor_score = self.minimax(successor_state, self.depth - 1, idx)
            if successor_score > max_score:
                max_score = successor_score
                optimal_actions = [action]
            elif successor_score == max_score:
                optimal_actions.append(action)
        if len(optimal_actions) > 1:
            return self.tiebreak(optimal_actions)[0]
        return optimal_actions[0] if len(optimal_actions) > 0 else False

    def tiebreak(actions: list):
        """
        Tiebreak: Method that takes in a list of list of tuples in the form [[(a, b), (c, d)], [(e, f), (g, h)]] where each
                sublist [(a, b), (c, d)] represents an action taken. This method prioritizes the lowest origin row coord,
                origin column coord, destination row coord, and destination column coord in that order. This method is
                guaranteed to return a single action [(a, b), (c, d)] because tiebreaking for lowest origin row coord
                and origin column coord guarantees that we've narrowed down the actions to only those which originate from
                (origin row coord, origin column coord). After tiebreaking for lowest destination row coord
                and destination column coord, we should've narrowed down the action to one origin and one destination.
                This method assumes that the list of actions passed in contains no duplicate actions.
        Params:
            actions: List - A list of actions in the form [[(a, b), (c, d)], [(e, f), (g, h)]], where (a, b) and (e, f)
                            represent the origin and (c, d) and (g, h) specify the destination.

        Output -> A list of tuples in the form [(a, b), (c, d)] representing the optimal action. (a, b) represents the origin
                and (c, d) represents the destination.
        """
        # Gets the penguin locations from the list of actions
        locations = [action for action in actions]
        # Sorts the list of locations in ascending order, with key being the row idx of the location
        locations.sort(key = lambda location: location[0][0])
        lowest_row_number = locations[0][0][0]
        # Gets all the locations that tied for row index
        locations = [location for location in locations if location[0][0] == lowest_row_number]

        # Sorts the list of locations in ascending order, with key being the column idx of the location
        locations.sort(key=lambda location: location[0][1])
        lowest_column_number = locations[0][0][1]
        # Gets all the locations that tied for column index
        locations = [location for location in locations if location[0][1] == lowest_column_number]

        # Sorts the list of locations in ascending order, with key being the row idx of the destination
        locations.sort(key=lambda location: location[1][0])
        lowest_row_number = locations[0][1][0]
        # Gets all the locations that tied for row index
        locations = [location for location in locations if location[1][0] == lowest_row_number]
        # Sorts the list of locations in ascending order, with key being the column idx of the destination
        locations.sort(key=lambda location: location[1][1])

        return locations

    def minimax(self, state: State, max_depth: int, player_idx: int):
        """
        minimax:  Returns the optimal "reward" for a player after max_depth number of turns, where the reward is the total
                score of the maximizing agent (current player). Minimax assumes both a minimizing and maximizing agents,
                where minimizing agents (other players) are trying to minimize the maximizing agent's reward,
                whereas maximizing agents are trying to maximize their own reward.

        Params:
            state: State - A state in which no more penguins will be placed.
            max_depth: int - An integer representing the number of turns that minimax will look forward to calculate the
                            optimal reward
            player_idx: int - An integer representing the turn index corresponding to the maximizing agent in the State
                            representation

        Output -> An integer representing the reward for the given state after a certain number of turns (max_depth)
        """
        if not state or max_depth == 0 or state.game_over():
            return state.get_players()[player_idx].get_score()
        elif state.get_turn_idx() == player_idx:
            return self.get_maximum_score(state, max_depth - 1, player_idx)
        else:
            return self.get_minimum_score(state, max_depth, player_idx)

    def get_maximum_score(self, state: State, max_depth: int, player_idx: int):
        """
        get_maximum_score: Helper function for minimax that gets the max score of all possible moves from the given state,
                        looking forward the specified number of turns.

        Params:
            state: State - A state in which no more penguins will be placed.
            max_depth: int - An integer representing the number of turns that minimax will look forward to calculate the
                            optimal reward
            player_idx: int - An integer representing the turn index corresponding to the maximizing agent in the State
                            representation

        Output -> An integer representing the max reward for the given state after a certain number of turns (max_depth)
        """
        max_score = float("-inf")
        node = GameTreeNode(state)
        for action in node.check_available_actions():
            max_score = max(
                self.minimax(node.generate_successor(action), max_depth, player_idx),
                max_score
            )
        return max_score

    def get_minimum_score(self, state: State, max_depth: int, player_idx: int):
        """
        get_minimum_score: Helper function for minimax that gets the min score of all possible moves from the given state,
                        looking forward the specified number of turns.

        Params:
            state: State - A state in which no more penguins will be placed.
            max_depth: int - An integer representing the number of turns that minimax will look forward to calculate the
                            optimal reward
            player_idx: int - An integer representing the turn index corresponding to the maximizing agent in the State
                            representation

        Output -> An integer representing the min reward for the given state after a certain number of turns (max_depth)
        """
        min_score = float("inf")
        node = GameTreeNode(state)
        for action in node.check_available_actions():
            min_score = min(
                self.minimax(node.generate_successor(action), max_depth, player_idx),
                min_score
            )
        return min_score

    def set_color(self, color: str):
        return True

    def set_other_players(self, colors: list):
        return True

    def start(self):
        return True

    def end(self, is_winner):
        return True

    def kill_client(self):
        pass


class RemoteStrategy(Strategy):
    
    def __init__(self, fish_client):
        self.fish_client = fish_client

    def get_placement(self, state: State):
        return self.fish_client.setup(state)

    def get_move(self, state: State, actions: list):
        return self.fish_client.take_turn(state, actions)

    def set_color(self, color: str):
        return self.fish_client.playing_as(color)

    def set_other_players(self, colors: list):
        return self.fish_client.playing_with(colors)

    def start(self):
        return self.fish_client.start()

    def end(self, is_winner):
        return self.fish_client.end(is_winner)

    def kill_client(self):
        self.fish_client.end_connection()