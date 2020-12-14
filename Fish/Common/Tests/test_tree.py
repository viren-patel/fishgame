import unittest
import sys
sys.path.insert(1, '../../')

from Common.game_tree import GameTreeNode
from Common.state import State
# from Common.utils import parse_json
class TestGameTreeNode(unittest.TestCase):

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
        self.state.place_penguin((4, 4))
        self.state.place_penguin((4, 3))
        self.state.place_penguin((4, 2))
        self.state.place_penguin((3, 4))
        self.state.place_penguin((3, 3))
        self.state.place_penguin((3, 2))
        self.state.place_penguin((2, 4))
        self.state.place_penguin((2, 3))
        self.state.place_penguin((2, 2))
        self.tree = GameTreeNode(self.state)

    def test_check_valid_move(self):
        self.assertTrue(self.tree.check_valid_move((2, 4), (0, 4)))
        self.assertFalse(self.tree.check_valid_move((3, 4), (0, 4)))

    def test_generate_successor(self):
        successor = self.tree.generate_successor([(2, 4), (0, 4)])
        players = [
            {
                "color": "blue",
                "score": 1,
                "places": [(4, 4), (3, 4), (0, 4)]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": [(4, 3), (3, 3), (2, 3)]
            },
            {
                "color": "red",
                "score": 0,
                "places": [(4, 2), (3, 2), (2, 2)]
            }
        ]
        tiles = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        expected_state = State(players, tiles, turn_index = 1)
        self.assertEqual(successor, expected_state)

    def test_generate_successor_placement(self):
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
        state = State(players, tiles)
        node = GameTreeNode(state)
        successor = node.generate_successor([(0, 0)])
        node = GameTreeNode(successor)
        successor = node.generate_successor([(0, 1)])
        node = GameTreeNode(successor)
        successor = node.generate_successor([(0, 2)])
        players = [
            {
                "color": "blue",
                "score": 0,
                "places": [[0, 0]]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": [[0, 1]]
            },
            {
                "color": "red",
                "score": 0,
                "places": [[0, 2]]
            }
        ]
        tiles = [
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]
        ]
        expected_state = State(players, tiles, turn_index = 0)
        self.assertEqual(successor, expected_state)
