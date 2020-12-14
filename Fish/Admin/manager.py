from Common.state import State, Game_Phase
from Common.game_tree import GameTreeNode
from Player.player import PlayerAI
from Common.player import Player
from Common.board import Board
from Admin.referee import Referee
from threading import Thread
from Remote.timeout import timeout


MAX_PLAYERS = 4
MIN_PLAYERS = 2
TIMEOUT_PERIOD = 1

class Tournament:
    """Represents a tournament manager for Fish Game for a given set of PlayerAI's. The tournament manager matches up players to games
       and creates referees to run those games. Informs the winner(s) of the tournament that they have won.
    """

    def __init__(self, players: list):
        self.remaining_players = players.copy()
        self.round_results = []
        self.cheating_players = set()
        self.failed_players = set()
        self.id_dict = self.get_id_dict(players)
        self.last = None

    @staticmethod
    def get_id_dict(players):
        """Creates a dictionary of player id to PlayerAI object

            parameters:
            players: List of PlayerAI

            output: Dictionary{uuid: PlayerAI}
        """
        ids = {}
        for player in players:
            ids[player.id] = player
        return ids

    def run_tournament(self):
        """Runs the tournament in its entirety until there are no more games to be played. Informs the winning players that they
           have won the tournament
        """
        self.notify_tournament_start()
        while not self.check_end():
            round_results = self.run_round()
            self.remaining_players = [self.id_dict[winner_id] for winner_id in round_results['winners']]
            self.round_results.append(self.remaining_players)
            self.cheating_players.update([self.id_dict[cheater_id] for cheater_id in round_results['cheaters']])
            self.failed_players.update([self.id_dict[failed_id] for failed_id in round_results['failed']])

        self.notify_tournament_end()

    def run_round(self):
        """Runs a single round of a tournament of Fish Game. First allocates each player remaining to a game and creates referees to run each game. Returns a
           list of the ids of the winning players

            output: List of uuid
        """
        self.last = self.remaining_players
        game_list = self.assign_games()
        game_count = len(game_list)
        winners = [[]] * game_count
        cheaters = [[]] * game_count
        failed = [[]] * game_count
        threads = []
        for i in range(game_count):
            new_thread = Thread(target=self.run_game, args=(game_list[i], i, winners, cheaters, failed))
            threads.append(new_thread)
            new_thread.start()
        for thread in threads:
            thread.join()
        # Flatten the lists of winners, cheaters, and failed players provided by the threads
        winners = [winner for sublist in winners for winner in sublist]
        cheaters = [cheater for sublist in cheaters for cheater in sublist]
        failed = [failed_player for sublist in failed for failed_player in sublist]
        return {"winners": winners, "cheaters": cheaters, "failed": failed}

    @staticmethod
    def run_game(players, output_index, winner_list, cheater_list, failed_list):
        ref = Referee(players)
        game_output = ref.run_game()
        try:
            winner_list[output_index] = game_output["winners"]
            cheater_list[output_index] = game_output["cheaters"]
            failed_list[output_index] = game_output["failed"]
            return True
        except IndexError:
            return False

    def assign_games(self):
        """Matches up players to games of size 2 <= number of players <= 4. Returns a list of list of players in a game

            output: List of List of PlayerAI
        """
        game_list = [[]]
        length = len(self.remaining_players)
        for i in range(length):
            if len(game_list[-1]) == MAX_PLAYERS:
                if len(self.remaining_players) < MIN_PLAYERS:
                    #Backtracking
                    for j in range(MIN_PLAYERS - len(self.remaining_players)):
                        # NOTE: Assumes there's enough prev games to only take one player 
                        # from each prev game to fill final game
                        self.remaining_players.insert(0, game_list[-1 - j][-1])
                        game_list[-1 - j].pop(-1)
                    game_list.append(self.remaining_players.copy())
                    break

                else:
                    game_list.append([])
            game_list[-1].append(self.remaining_players.pop(0))
        return game_list

    def check_end(self):
        """Returns True if the whole tournament is over.

            output: boolean
        """
        no_games_possible = len(self.remaining_players) < MIN_PLAYERS
        repeated_winners = self.last is not None and self.remaining_players == self.last
        showdown_complete = self.last is not None and len(self.last) <= MAX_PLAYERS
        return no_games_possible or repeated_winners or showdown_complete

    def is_contactable(self, player):
        """
        Checks whether contacting this player is allowed, e.g. the player is not failing or cheating.

        :param player: The PlayerAI to check.
        :return: True if it's contactable, false otherwise
        """
        return player not in self.cheating_players and player not in self.failed_players

    def notify_tournament_start(self):
        players = self.remaining_players
        for player in players:
            success = timeout(TIMEOUT_PERIOD, player.inform_start, [])
            if success is None or not success:
                self.fail_player(player)

    def notify_tournament_end(self):
        """informs contactable Players whether they have won the tournament
        """
        for player in self.id_dict.values():
            is_winner = player in self.remaining_players
            if self.is_contactable(player):
                success = timeout(TIMEOUT_PERIOD, player.inform_end, [is_winner])
                if success is None or not success:
                    self.fail_player(player)

    def fail_player(self, player):
        if player in self.remaining_players:
            self.remaining_players.remove(player)
        player.inform_remove()
        self.failed_players.add(player)
