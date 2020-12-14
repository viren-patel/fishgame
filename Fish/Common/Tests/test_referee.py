import unittest
import sys
sys.path.insert(1, '../../')

from Common.state import State, Game_Phase
from Admin.referee import Referee
from Player.player import PlayerAI
from unittest.mock import MagicMock

class ErrorPlayer:
    def __init__(self):
        self.state = None
    def update_state(self, state: State):
        self.state = None
    def set_turn_idx(self, i):
        self.state = None

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
        ]
        self.referee = Referee(players)

    def test_constructor(self):
        self.assertEqual(len(self.referee.state.get_board_tiles()), 5)
        self.assertEqual(len(self.referee.state.get_board_tiles()[0]), 5)
        self.assertEqual(self.referee.state.players[0].toDict(),
            {'color' : 'r',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.state.players[1].toDict(),
            {'color' : 'g',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.state.players[2].toDict(),
            {'color' : 'b',
             'score' : 0,
             'places' : []})

    def test_run_placement(self):
        self.referee.run_placement()
        self.assertEqual(self.referee.state.get_game_phase(),Game_Phase.PLAYING)
        self.assertEqual(self.referee.state.players[0].toDict(),
            {'color' : 'r',
             'score' : 0,
             'places' : [(0, 0), (0, 3), (1, 1)]})
        self.assertEqual(self.referee.state.players[1].toDict(),
            {'color' : 'g',
             'score' : 0,
             'places' : [(0, 1), (0, 4), (1, 2)]})
        self.assertEqual(self.referee.state.players[2].toDict(),
            {'color' : 'b',
             'score' : 0,
             'places' : [(0, 2), (1, 0), (1, 3)]})


    def test_run(self):
        self.referee.run_game()
        self.assertEqual(self.referee.state.get_game_phase(),Game_Phase.GAME_OVER)


    def test_remove_player(self):
        self.referee.remove_player(0)
        self.assertEqual(self.referee.state.players[0].toDict(),
            {'color' : 'g',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.state.players[1].toDict(),
            {'color' : 'b',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.players[0].turn_idx, 0)

    def test_remove_cheater(self):
        self.referee.update_game_state([[-1,0]],0)
        self.assertEqual(self.referee.state.players[0].toDict(),
            {'color' : 'g',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.state.players[1].toDict(),
            {'color' : 'b',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.players[0].turn_idx, 0)

    def test_player_error(self):
        players = [
            ErrorPlayer(),
            PlayerAI(1),
            PlayerAI(2),
        ]
        ref = Referee(players)
        ref.run_placement()
        self.assertEqual(ref.state.get_game_phase(),Game_Phase.PLAYING)
        self.assertEqual(ref.state.players[0].toDict(),
            {'color' : 'g',
             'score' : 0,
             'places' : [(0, 0), (0, 2), (0, 4), (1,1)]})
        self.assertEqual(ref.state.players[1].toDict(),
            {'color' : 'b',
             'score' : 0,
             'places' : [(0, 1), (0, 3), (1,0), (1,2)]})


    def test_update_game_state(self):
        self.referee.update_game_state([[0,0]],0)
        self.assertEqual(self.referee.state.players[0].toDict(),
            {'color' : 'r',
             'score' : 0,
             'places' : [(0,0)]})
        self.assertEqual(self.referee.state.players[1].toDict(),
            {'color' : 'g',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.state.players[2].toDict(),
            {'color' : 'b',
             'score' : 0,
             'places' : []})
        self.assertEqual(self.referee.players[0].state.players[0].toDict(),
            {'color' : 'r',
             'score' : 0,
             'places' : [(0,0)]})
