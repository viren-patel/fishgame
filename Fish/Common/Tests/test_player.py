import unittest
import sys
sys.path.insert(1, '../../')

from Common.state import State, Game_Phase
from Admin.referee import Referee
from Player.player import PlayerAI

# from Common.utils import parse_json
class TestPlayer(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.state = None

    def test_equality(self):
        players = [
            {
                "color": "blue",
                "score": 0,
                "places": [(0, 0), (0, 3), (1, 1)]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": [(0, 1), (0, 4), (1, 2)]
            },
            {
                "color": "red",
                "score": 0,
                "places": [(0, 2), (1, 0), (1, 3)]
            }
        ]
        tiles = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        state = State(players, tiles, game_phase = Game_Phase.PLAYING)
        player = PlayerAI(0)
        player.update_state(state)

        players2 = [
            {
                "color": "blue",
                "score": 0,
                "places": [(0, 0), (0, 3), (1, 1)]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": [(0, 1), (0, 4), (1, 2)]
            },
            {
                "color": "red",
                "score": 0,
                "places": [(0, 2), (1, 0), (1, 3)]
            }
        ]
        tiles2 = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        state2 = State(players2, tiles2, game_phase=Game_Phase.PLAYING)
        player2 = PlayerAI(0)
        player2.update_state(state2)
        self.assertEqual(player, player2)

