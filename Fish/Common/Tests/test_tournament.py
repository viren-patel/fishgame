import unittest
import sys
sys.path.insert(1, '../../')
from Common.state import State, Game_Phase
from Admin.referee import Referee
from Player.player import PlayerAI
from unittest.mock import MagicMock
from Admin.manager import Tournament
import uuid

class ErrorPlayer:
    def __init__(self):

        self.id = uuid.uuid1()
        self.state = None
    def update_state(self, state: State):
        self.state = None
    def set_turn_idx(self, i):
        self.state = None
    def inform_win(self):
        return False


# from Common.utils import parse_json
class TestReferee(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.state = None


    def setUp(self):
        players = [
                    PlayerAI(0),
                    PlayerAI(1),
                    PlayerAI(2),
                    PlayerAI(3),
                    PlayerAI(4),
                    PlayerAI(5),
                    PlayerAI(6),
                    PlayerAI(7),
                    PlayerAI(8),
                    PlayerAI(9),
                    PlayerAI(10),
     ]
        self.tournament = Tournament(players)

    def test_run_all(self):
        self.tournament.run_tournament()
        self.assertEqual(len(self.tournament.remaining_players) < 3, True)

    def test_assign_games(self):
        game_list = self.tournament.assign_games()
        self.assertEqual(game_list,
                         [[PlayerAI(0),
                           PlayerAI(1),
                           PlayerAI(2),
                           PlayerAI(3)],
                          [PlayerAI(4),
                           PlayerAI(5),
                           PlayerAI(6),
                           PlayerAI(7)],
                          [PlayerAI(8),
                           PlayerAI(9),
                           PlayerAI(10)]])
        players = [
                    PlayerAI(0),
                    PlayerAI(1),
                    PlayerAI(2),
                    PlayerAI(3),
                    PlayerAI(4),
                    PlayerAI(5),
                    PlayerAI(6),
                    PlayerAI(7),
                    PlayerAI(8),
                    ]
        new_tournament = Tournament(players)
        self.assertEqual(new_tournament.assign_games(),
                         [[PlayerAI(0),
                           PlayerAI(1),
                           PlayerAI(2),
                           PlayerAI(3)],
                          [PlayerAI(4),
                           PlayerAI(5),
                           PlayerAI(6)],
                          [PlayerAI(7),
                           PlayerAI(8)]])

    def test_inform_winners(self):
        players = [
                    ErrorPlayer(),
                    PlayerAI(1),
                    PlayerAI(2)
        ]
        tournament = Tournament(players)
        tournament.inform_winners()


        self.assertEqual(tournament.players, [PlayerAI(1),
                                         PlayerAI(2)])

    def test_check_end(self):
        self.assertEqual(self.tournament.check_end(), False)


        players_same_winners = [
                              PlayerAI(0),
                              PlayerAI(1),
                              PlayerAI(2),
                              PlayerAI(3)
                             ]
        tournament_same_winners = Tournament(players_same_winners)
        tournament_same_winners.last = players_same_winners
        self.assertEqual(tournament_same_winners.check_end(), True)

        not_enough_players = [PlayerAI(0)]
        not_enough_players_tournament = Tournament(not_enough_players)
        self.assertEqual(not_enough_players_tournament.check_end(), True)

        final_round =  [
                        PlayerAI(0),
                        PlayerAI(1),
                        PlayerAI(2),
                        PlayerAI(3)
                        ]
        final_round_tournament = Tournament(final_round)
        self.assertEqual(final_round_tournament.check_end(), False)
