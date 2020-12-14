import unittest
import sys
sys.path.insert(1, '../../')

from Common.state import State
from Common.game_tree import GameTreeNode
from Player.strategy import place_penguin, get_optimal_action
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
            }
        ]
        tiles = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]
        self.state = State(players, tiles)

    def test_place_penguin(self):
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
            }
        ]
        tiles = [
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1]
        ]
        self.state = State(players, tiles)
        placement = place_penguin(self.state)
        self.assertEqual(placement, [(0, 0)])
        self.state = GameTreeNode(self.state).generate_successor(placement)
        placement = place_penguin(self.state)
        self.assertEqual(placement, [(0, 2)])
        self.state = GameTreeNode(self.state).generate_successor(placement)
        placement = place_penguin(self.state)
        self.assertEqual(placement, [(0, 4)])
        self.state = GameTreeNode(self.state).generate_successor(placement)
        placement = place_penguin(self.state)
        self.assertEqual(placement, [(1, 0)])
        self.state = GameTreeNode(self.state).generate_successor(placement)
        placement = place_penguin(self.state)
        self.assertEqual(placement, [(1, 2)])


    # def test_get_optimal_action(self):
    #     players = [
    #         {
    #             "color": "blue",
    #             "score": 0,
    #             "places": [(0, 0), (0, 2), (1, 1), (2, 0)]
    #         },
    #         {
    #             "color": "yellow",
    #             "score": 0,
    #             "places": [(0, 1), (1, 0), (1, 2), (2, 1)]
    #         }
    #     ]
    #     tiles = [
    #         [1, 1, 1],
    #         [1, 1, 1],
    #         [1, 1, 1]
    #     ]
    #     self.state = State(players, tiles)
    #     node = GameTreeNode(self.state)
    #     self.assertEqual(get_optimal_action(node), [(0, 2), (2, 2)])


    # def test_get_optimal_action_bigger_board(self):
    #     players = [
    #         {
    #             "color": "blue",
    #             "score": 0,
    #             "places": []
    #         },
    #         {
    #             "color": "yellow",
    #             "score": 0,
    #             "places": []
    #         }
    #     ]
    #     tiles = [
    #         [1, 1, 1, 1],
    #         [1, 1, 1, 1],
    #         [1, 1, 1, 1],
    #         [1, 1, 1, 1]
    #     ]
    #     self.state = State(players, tiles)
    #     auto_place_penguins(self.state)
    #     node = GameTreeNode(self.state)
    #     self.assertEqual(get_optimal_action(node), [(0, 0), (2, 0)])
    #     self.assertEqual(get_optimal_action(node, depth=4), [(0, 0), (2, 0)])

    def test_get_optimal_action_game_over(self):
        players = [
            {
                "color": "blue",
                "score": 0,
                "places": [(0, 0), (0, 2), (1, 0), (1, 2)]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": [(0, 1), (0, 3), (1, 1), (1, 3)]
            }
        ]
        tiles = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.state = State(players, tiles)
        node = GameTreeNode(self.state)
        self.assertEqual(get_optimal_action(node), None)

        players = [
            {
                "color": "blue",
                "score": 0,
                "places": [(0, 0)]
            },
            {
                "color": "yellow",
                "score": 0,
                "places": []
            }
        ]
        tiles = [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.state = State(players, tiles)
        node = GameTreeNode(self.state)
        self.assertEqual(get_optimal_action(node), None)
