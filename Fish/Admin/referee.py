from Remote.timeout import timeout, TIMEOUT_PERIOD
from Common.state import State, Game_Phase
from Common.game_tree import GameTreeNode
from Player.player import PlayerAI
from Common.player import Player
from Common.board import Board

# List of Player Colors:
colors = ['red', 'brown', 'black', 'white']

#TODO: Add a timeout for requesting action from player

def make_referee_same_fish(players, row, col, fish_per_tile, holes=None):
    if holes is None:
        holes = []
    tile_list = []
    for i in range(0, row):
        cur_row = []
        for j in range(0, col):
            cur_row.append(fish_per_tile)
        tile_list.append(cur_row)

    valid_val = lambda x, max_val: x > 0 and x < max_val
    for coord in holes:
        if valid_val(coord[0], row) and valid_val(coord[1], col):
            tile_list[coord[0]][coord[1]] = 0
    
    new_player_list = []
    for i in range(len(players)):
        player = {'color': colors[i], 'score': 0, 'places': []}
        new_player_list.append(player)
    state = State(new_player_list, tile_list)
    ref = Referee(players)
    ref.state = state
    return ref


class Referee:
    """
    Implementation of a Referee used by the tournament system to run an individual game.
    After being initialized, the Referee waits for run_game to be called.  run_game causes the referee to run the full length of the game,
    prompting players to place penguins and make moves.  If a player cheats in any way, the referee removes the player from the game.  After the game has ended, and no
    player is able to make a valid move, the referee reports the scores to both the player and the tournament.  A referee can only be used once.
    """

    def __init__(self, players: list):
        """
            __init__ - Creates a referee given the initial state the referee is expected to run.  This function
                       creates the PlayerAIs necessary to play the game.

            Parameters:
            Mandatory:
                state - A State representing the game the referee is expected to run

            Output -> A Referee prepared to play the current state, with PlayerAI of the given depth.
        """
        self.players = players
        self.cheaters = []
        self.failed = []
        self.action_queue_dict = dict()
        [self.players[i].set_turn_idx(i) for i in range(0, len(self.players))]
        for player in self.players:
            self.action_queue_dict[player.id] = []
        self.state = self.makestate()
        self.update_player_state()

    def makestate(self):
        """ makestate - Makes a Random Starting Gamestate for  this referee.

            Output -> A Gamestate with a random 5x5 board for this referee.
        """
        new_player_list = []
        for i in range(len(self.players)):
            player = {'color': colors[i], 'score': 0, 'places': []}
            new_player_list.append(player)
        return State(new_player_list, Board.make_random_board(5, 5).get_board())

    def run_placement(self):
        while self.state.get_game_phase() == Game_Phase.PLACEMENT:
            if len(self.state.players):
                self.state.game_phase = Game_Phase.GAME_OVER
            turn_idx = self.state.get_turn_idx()
            player = self.players[turn_idx]
            placement = timeout(TIMEOUT_PERIOD, player.get_placement, [])
            if placement is None:
                self.remove_player(turn_idx, False)
                self.update_player_state()
            else:
                self.update_game_state(placement, turn_idx)


    def run_playing(self):
        while self.state.get_game_phase() == Game_Phase.PLAYING:
            if len(self.state.players) == 0:
                self.state.game_phase = Game_Phase.GAME_OVER
            turn_idx = self.state.get_turn_idx()
            player = self.players[turn_idx]
            action_queue = self.action_queue_dict[player.id]
            move = timeout(TIMEOUT_PERIOD, player.get_next_move, [action_queue])
            action_queue.clear()
            if move is None:
                self.remove_player(turn_idx, False)
                self.update_player_state()
            else:
                for id in self.action_queue_dict:
                    if id != player.id:
                        self.action_queue_dict[id].append(placement)
                self.update_game_state(move, turn_idx)

    def inform_colors(self):
        players = self.players
        colors = [player.get_color() for player in self.state.players]
        idx = 0
        while idx < len(players):
            player = players[idx]
            success = timeout(TIMEOUT_PERIOD, player.inform_color, [colors[idx]])
            if success is None or not success:
                self.remove_player(idx, False)
            else:
                idx += 1
            
    def inform_player_opponents(self):
        players = self.players
        colors = [player.get_color() for player in self.state.players]
        idx = 0
        while idx < len(players):
            player = players[idx]
            opponents = colors.copy()
            opponents.pop(idx)
            success = timeout(TIMEOUT_PERIOD, player.inform_opponents, [opponents])
            if success is None or not success:
                self.remove_player(idx, False)
            else:
                idx += 1

    # TODO: Might have to rework how this is done
    def run_game(self):
        """
            run_game - Runs the game for the given state and playerAIs.

            This function checks the current game_phase of the gamestate and acts accordningly.
                If the game_phase is in placements the function will continue to request placements from players before moving the the playing phase
                If the game_phase is in playing the function will continue to request moves from players until no more moves can be made by any player.
                    The function then moves the the game over phase.
                In the Game over phase, the function reports to the players the final game state, and reports the score to the tournament.
        """
        self.update_player_state()
        self.inform_colors()
        self.inform_player_opponents()
        self.run_placement()
        self.run_playing()
        if self.state.get_game_phase() == Game_Phase.GAME_OVER:
            self.update_player_state()
            winners = self.get_winner()
            return {'winners': winners, 'cheaters': [cheater for cheater in self.cheaters], 'failed': [failedp for failedp in self.failed]}
            # self.report_score()

    def get_winner(self):
        # Returns a list the ids of the winning player(s)
        player_list = self.state.players

        cur_best_players = [self.players[0].id]
        cur_max = player_list[0].score
        for i in range(1, len(player_list)):
            if player_list[i].score > cur_max:
                cur_best_players = [self.players[i].id]
                cur_max = player_list[i].score
            elif player_list[i].score == cur_max:
                cur_best_players.append(self.players[i].id)
        
        return cur_best_players

    def update_player_state(self):
        """
            update_player_state - This function updates the playerAIs with the current gamestate that the referee has.
                This function is called each time the gamestate changes, and at the end of the game.
        """
        for player in self.players:
            player.update_state(self.state)

    def update_game_state(self, action: list, turn_idx: int):
        """
            update_game_state - This function updates the gamestate of the Referee when a player makes an action.
                If the given action is considered cheating, the player is removed from the game.

            Parameters:
                action - An action is a list containing either:
                - a single tuple [(row,col)] representing the row and col coordinates of the players next penguin
                  placement one the board
                - two tuples [(origin-row, origin-col),(dest-row,dest-col)] where the first tuple represents the current
                  position of the penguin and the second tuple represents the destination of the move.
                - turn_idx - An integer representing the player with the current turn.
        """
        new_state = self.generate_successor(action)
        if new_state:
            self.state = new_state
        else:
            self.remove_player(turn_idx, True)
        self.update_player_state()

    def remove_player(self, turn_idx: int, is_cheater: bool):
        """
            remove_player - This function removes a cheating player from the game
                This removes all of the players penguins, and deletes their score.
                It also informs necessary other players that the player has been disqualified so they
                can decrement their turn_idx. A game will keep going until no players can move.

            Player is cheating if one of the following actions are issued:
                - Placing a penguin when the game phase is not in PLACEMENT
                - Placing a penguin on a tile that does not exist on the board (invalid row/col)
                - Placing a penguin on a tile that is a hole or occupied by another player
                - Moving a penguin when the game phase is not in PLAYING
                - Moving a penguin when it is not the player's turn
                - Moving a penguin to a tile that does not exist on the board
                - Moving a penguin that does not exist for the current player
                - Moving a penguin in a direction that is not a straight line from the origin
                - Moving a penguin over/on a space that is a hole or occupied by another penguin
            Player is also Cheating if one of the following errors occurs:
                - Calling for the next move or placement results in an exception
                - Player Does not respond
                - Player mutates data structures (This will not happen?)
        """
        for i in range(turn_idx + 1, len(self.players)):
            self.players[i].decrement_turn_idx()
        self.state.remove_player(turn_idx)
        if is_cheater:
            self.cheaters.append(self.players[turn_idx].id)
        else:
            self.failed.append(self.players[turn_idx].id)
        self.players[turn_idx].inform_remove()
        self.players.pop(turn_idx)
        for player in self.players:
            self.action_queue_dict[player.id].clear()

    def generate_successor(self, action):
        """
            generate_successor - returns the next state for the referee given that the action was valid.  Returns None otherwise.

            Parameters:
            action - An action is a list containing either:
                - a single tuple [(row,col)] representing the row and col coordinates of the players next penguin
                  placement one the board
                - two tuples [(origin-row, origin-col),(dest-row,dest-col)] where the first tuple represents the current
                  position of the penguin and the second tuple represents the destination of the move.

            Output ->
                Either
                    A State represnting the new state after the given action has taken placement
                Or
                    None if the action is an invalid move.

        """
        node = GameTreeNode(self.state)
        return node.generate_successor(action)

    def report_score(self):
        """
            report_score - Function for reporting the score to the tournament, and remote players.
                Due to this functionality of tournaments and remote players not being supported yet, this function does nothing for now.
        """
        print("")
