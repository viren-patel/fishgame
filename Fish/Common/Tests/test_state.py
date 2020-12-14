import unittest
import sys
sys.path.insert(1, '../../')

from Common.state import State
# from Common.utils import parse_json
class TestState(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.state = None

    def setUp(self):
        players = [
            {
                "color": "blue",
                "score": 0,
                "places": []
            },
            {
                "color": "yellow",
                "score": 0,
                "places": []
            },
            {
                "color": "red",
                "score": 0,
                "places": []
            }
        ]
        tiles = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        self.state = State(players, tiles)

    def test_from_state(self):
        new_state = State.from_state(self.state)
        self.assertTrue(self.state == new_state)

    def test_can_player_move(self):
        players = [
            {
                "color": "blue",
                "score": 0,
                "places": [[0, 0]]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": [[1, 1]]
            },
            {
                "color": "red",
                "score": 0,
                "places": [[2, 2]]
            }
        ]
        tiles = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        state = State(players, tiles)
        self.assertTrue(state.can_player_move(0))
        self.assertTrue(state.can_player_move(1))
        self.assertTrue(state.can_player_move(2))

    def test_place_penguin(self):
        self.state.place_penguin((4, 4))
        self.state.place_penguin((4, 3))
        self.state.place_penguin((4, 2))
        players = self.state.get_players()
        self.assertEqual(players[0].get_penguin_locations(), [(4, 4)])
        self.assertEqual(players[1].get_penguin_locations(), [(4, 3)])
        self.assertEqual(players[2].get_penguin_locations(), [(4, 2)])
        self.assertFalse(self.state.board.check_valid_tile(4, 4))
        self.assertFalse(self.state.board.check_valid_tile(4, 3))
        self.assertFalse(self.state.board.check_valid_tile(4, 2))

    def test_move_penguin(self):
        self.state.place_penguin((4, 4))
        self.state.place_penguin((4, 3))
        self.state.place_penguin((4, 2))
        self.assertRaises(ValueError, self.state.move_penguin, (4, 3), (2, 3))
        self.state.place_penguin((3, 4))
        self.state.place_penguin((3, 3))
        self.state.place_penguin((3, 2))
        self.state.place_penguin((2, 4))
        self.state.place_penguin((2, 3))
        self.state.place_penguin((2, 2))

        self.state.move_penguin((2, 4), (0, 4))
        self.assertEqual(self.state.get_turn_idx(), 1)
        self.assertEqual(self.state.players[0].get_penguin_locations(), [(4, 4), (3, 4), (0, 4)])
        self.assertEqual(self.state.players[0].get_score(), 1)
        self.assertFalse(self.state.board.check_valid_tile(2, 4))

        self.state.move_penguin((2, 3), (0, 3))
        self.assertEqual(self.state.get_turn_idx(), 2)
        self.assertEqual(self.state.players[1].get_penguin_locations(), [(4, 3), (3, 3), (0, 3)])
        self.assertEqual(self.state.players[1].get_score(), 1)
        self.assertFalse(self.state.board.check_valid_tile(2, 3))

        self.state.move_penguin((2, 2), (0, 2))
        self.assertEqual(self.state.get_turn_idx(), 0)
        self.assertEqual(self.state.players[2].get_penguin_locations(), [(4, 2), (3, 2), (0, 2)])
        self.assertEqual(self.state.players[2].get_score(), 1)
        self.assertFalse(self.state.board.check_valid_tile(2, 2))

    def test_get_valid_moves(self):
        self.state.place_penguin((4, 4))
        self.state.place_penguin((4, 3))
        self.state.place_penguin((4, 2))
        self.state.place_penguin((3, 4))
        self.state.place_penguin((3, 3))
        self.state.place_penguin((3, 2))
        self.state.place_penguin((2, 4))
        self.state.place_penguin((2, 3))
        self.state.place_penguin((2, 2))
        expected = [[(3, 4), (1, 4)], [(2, 4), (0, 4)], [(2, 4), (1, 4)], [(2, 4), (1, 3)], [(2, 4), (0, 3)]]
        self.assertEqual(self.state.get_valid_moves(), expected)
