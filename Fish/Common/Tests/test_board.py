
import unittest
import sys
sys.path.insert(1, '../../')

from Common.board import Board
# from Common.utils import parse_json
class TestBoard(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    """
    Tests that make_board_from_tiles properly constructs a board from the given tiles.
    """
    def test_make_board_from_tiles(self):
        tiles = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        board = Board.make_board_from_tiles(tiles)
        self.assertEqual(tiles, board.get_board())

    """
    Tests that make_random_board constructs a random board.
    """
    def test_make_random_board(self):
        board = Board.make_random_board(5, 4)
        tiles = board.get_board()
        self.assertEqual(5, len(tiles))
        self.assertEqual(4, len(tiles[0]))
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                self.assertTrue(tiles[i][j] >= 1 and tiles[i][j] <= 5)

    """
    Tests that make_random_board constructs a random board with holes.
    """
    def test_make_random_board_with_holes(self):
        holes = [(0, 0), (1, 1), (2, 2), (3, 3)]
        board = Board.make_random_board(4, 4, holes=holes)
        tiles = board.get_board()
        self.assertEqual(4, len(tiles))
        self.assertEqual(4, len(tiles[0]))
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if (i, j) not in holes:
                    self.assertTrue(tiles[i][j] >= 1 and tiles[i][j] <= 5)
                else:
                    self.assertTrue(tiles[i][j] == 0)

    """
    Tests that make_random_board constructs a random board with a minimum number of tiles that contain 1 fish.
    """
    def test_make_random_board_with_min_ones(self):
        min_ones = 10
        board = Board.make_random_board(4, 4, min_ones=min_ones)
        tiles = board.get_board()
        self.assertEqual(4, len(tiles))
        self.assertEqual(4, len(tiles[0]))
        count = 0
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                    self.assertTrue(tiles[i][j] >= 1 and tiles[i][j] <= 5)
                    if tiles[i][j] == 1:
                        count = count + 1
        self.assertTrue(count >= min_ones)

    """
    Tests that make_uniform_board constructs a uniform board.
    """

    def test_make_uniform_board(self):
        board = Board.make_uniform_board(5, 4, 3)
        tiles = board.get_board()
        self.assertEqual(5, len(tiles))
        self.assertEqual(4, len(tiles[0]))
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                self.assertTrue(tiles[i][j] == 3)

    """
    Tests that remove_tile correctly creates a hole at the specified x and y coordinate in the board, and that the method
    is idempotent.
    """

    def test_remove_tile(self):
        board = Board.make_uniform_board(5, 4, 3)
        tiles = board.get_board()
        self.assertEqual(5, len(tiles))
        self.assertEqual(4, len(tiles[0]))
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                self.assertTrue(tiles[i][j] == 3)

        board.remove_tile(0, 0)
        board.remove_tile(1, 1)
        tiles = board.get_board()
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if (i, j) == (0, 0) or (i, j) == (1, 1):
                    self.assertTrue(tiles[i][j] == 0)
                else:
                    self.assertTrue(tiles[i][j] == 3)

        board.remove_tile(0, 0)
        tiles = board.get_board()
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if (i, j) == (0, 0) or (i, j) == (1, 1):
                    self.assertTrue(tiles[i][j] == 0)
                else:
                    self.assertTrue(tiles[i][j] == 3)


    """
    Tests that check_valid_tile returns true when provided the coordinates of a valid tile and returns false when
    provided the coordinates of a hole.
    """

    def test_check_valid_tile(self):
        holes = [(0, 0), (1, 1), (2, 2), (3, 3)]
        board = Board.make_random_board(4, 4, holes=holes)
        tiles = board.get_board()
        self.assertEqual(4, len(tiles))
        self.assertEqual(4, len(tiles[0]))
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                if (i, j) in holes:
                    self.assertFalse(board.check_valid_tile(i, j))
                else:
                    self.assertTrue(board.check_valid_tile(i, j))


    def test_reachable_spaces_north(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces_north(0, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_north(1, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_north(2, 0)
        self.assertTrue(spaces == [(0, 0)])

        spaces = board.reachable_spaces_north(3, 0)
        self.assertTrue(spaces == [(1, 0)])

        spaces = board.reachable_spaces_north(4, 0)
        self.assertTrue(spaces == [(2, 0), (0, 0)])

        spaces = board.reachable_spaces_north(4, 0, depth=1)
        self.assertTrue(spaces == [(2, 0)])

        spaces = board.reachable_spaces_north(4, 0, depth=2)
        self.assertTrue(spaces == [(2, 0), (0, 0)])

        spaces = board.reachable_spaces_north(4, 0, depth=3)
        self.assertTrue(spaces == [(2, 0), (0, 0)])

        board.remove_tile(2, 0)
        spaces = board.reachable_spaces_north(4, 0)
        self.assertTrue(len(spaces) == 0)


    def test_reachable_spaces_northeast(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces_northeast(0, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_northeast(1, 0)
        self.assertTrue(spaces == [(0, 1)])

        spaces = board.reachable_spaces_northeast(2, 0)
        self.assertTrue(spaces == [(1, 0), (0, 1)])

        spaces = board.reachable_spaces_northeast(3, 0)
        self.assertTrue(spaces == [(2, 1), (1, 1), (0, 2)])

        spaces = board.reachable_spaces_northeast(4, 0)
        self.assertTrue(spaces == [(3, 0), (2, 1), (1, 1), (0, 2)])

        spaces = board.reachable_spaces_northeast(4, 0, depth=1)
        self.assertTrue(spaces == [(3, 0)])

        spaces = board.reachable_spaces_northeast(4, 0, depth=2)
        self.assertTrue(spaces == [(3, 0), (2, 1)])

        spaces = board.reachable_spaces_northeast(4, 0, depth=4)
        self.assertTrue(spaces == [(3, 0), (2, 1), (1, 1), (0, 2)])

        spaces = board.reachable_spaces_northeast(4, 0, depth=5)
        self.assertTrue(spaces == [(3, 0), (2, 1), (1, 1), (0, 2)])

        board.remove_tile(1, 1)
        spaces = board.reachable_spaces_northeast(4, 0)
        self.assertTrue(spaces == [(3, 0), (2, 1)])

    def test_reachable_spaces_southeast(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces_southeast(0, 0)
        self.assertTrue(spaces == [(1, 0), (2, 1), (3, 1), (4, 2)])

        spaces = board.reachable_spaces_southeast(1, 0)
        self.assertTrue(spaces == [(2, 1), (3, 1), (4, 2)])

        spaces = board.reachable_spaces_southeast(0, 1)
        self.assertTrue(spaces == [(1, 1), (2, 2), (3, 2), (4, 3)])

        spaces = board.reachable_spaces_southeast(0, 2)
        self.assertTrue(spaces == [(1, 2), (2, 3), (3, 3), (4, 4)])

        spaces = board.reachable_spaces_southeast(0, 2, depth=1)
        self.assertTrue(spaces == [(1, 2)])

        spaces = board.reachable_spaces_southeast(0, 2, depth=2)
        self.assertTrue(spaces == [(1, 2), (2, 3)])

        spaces = board.reachable_spaces_southeast(0, 2, depth=4)
        self.assertTrue(spaces == [(1, 2), (2, 3), (3, 3), (4, 4)])

        spaces = board.reachable_spaces_southeast(0, 2, depth=5)
        self.assertTrue(spaces == [(1, 2), (2, 3), (3, 3), (4, 4)])

        board.remove_tile(3, 1)
        spaces = board.reachable_spaces_southeast(0, 0)
        self.assertTrue(spaces == [(1, 0), (2, 1)])

    def test_reachable_spaces_south(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces_south(0, 0)
        self.assertTrue(spaces == [(2, 0), (4, 0)])

        spaces = board.reachable_spaces_south(1, 0)
        self.assertTrue(spaces == [(3, 0)])

        spaces = board.reachable_spaces_south(2, 0)
        self.assertTrue(spaces == [(4, 0)])

        spaces = board.reachable_spaces_south(3, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_south(0, 0, depth=1)
        self.assertTrue(spaces == [(2, 0)])

        spaces = board.reachable_spaces_south(0, 0, depth=2)
        self.assertTrue(spaces == [(2, 0), (4, 0)])

        spaces = board.reachable_spaces_south(0, 0, depth=10)
        self.assertTrue(spaces == [(2, 0), (4, 0)])

        board.remove_tile(4, 0)
        spaces = board.reachable_spaces_south(0, 0)
        self.assertTrue(spaces == [(2, 0)])

    def test_reachable_spaces_southwest(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces_southwest(0, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_southwest(1, 0)
        self.assertTrue(spaces == [(2, 0)])

        spaces = board.reachable_spaces_southwest(0, 1)
        self.assertTrue(spaces == [(1, 0), (2, 0)])

        spaces = board.reachable_spaces_southwest(0, 2)
        self.assertTrue(spaces == [(1, 1), (2, 1), (3, 0), (4, 0)])

        spaces = board.reachable_spaces_southwest(4, 4)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_southwest(0, 2, depth=1)
        self.assertTrue(spaces == [(1, 1)])

        spaces = board.reachable_spaces_southwest(0, 2, depth=2)
        self.assertTrue(spaces == [(1, 1), (2, 1)])

        spaces = board.reachable_spaces_southwest(0, 2, depth=10)
        self.assertTrue(spaces == [(1, 1), (2, 1), (3, 0), (4, 0)])

        board.remove_tile(2, 1)
        spaces = board.reachable_spaces_southwest(0, 2)
        self.assertTrue(spaces == [(1, 1)])


    def test_reachable_spaces_northwest(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces_northwest(0, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_northwest(1, 0)
        self.assertTrue(spaces == [(0, 0)])

        spaces = board.reachable_spaces_northwest(2, 0)
        self.assertTrue(len(spaces) == 0)

        spaces = board.reachable_spaces_northwest(4, 4)
        self.assertTrue(spaces == [(3, 3), (2, 3), (1, 2), (0, 2)])

        spaces = board.reachable_spaces_northwest(4, 4, depth=1)
        self.assertTrue(spaces == [(3, 3)])

        spaces = board.reachable_spaces_northwest(4, 4, depth=2)
        self.assertTrue(spaces == [(3, 3), (2, 3)])

        spaces = board.reachable_spaces_northwest(4, 4, depth=float("inf"))
        self.assertTrue(spaces == [(3, 3), (2, 3), (1, 2), (0, 2)])

        board.remove_tile(1, 2)
        spaces = board.reachable_spaces_northwest(4, 4)
        self.assertTrue(spaces == [(3, 3), (2, 3)])

    def test_reachable_spaces(self):
        board = Board.make_uniform_board(5, 5, 1)

        spaces = board.reachable_spaces(0, 0)
        self.assertTrue(spaces == [(1, 0), (2, 1), (3, 1), (4, 2), (2, 0), (4, 0)])

        spaces = board.reachable_spaces(0, 0, depth=1)
        self.assertTrue(spaces == [(1, 0), (2, 0)])

        spaces = board.reachable_spaces(0, 0, depth=2)
        self.assertTrue(spaces == [(1, 0), (2, 1), (2, 0), (4, 0)])

        spaces = board.reachable_spaces(0, 0, depth=float("inf"))
        self.assertTrue(spaces == [(1, 0), (2, 1), (3, 1), (4, 2), (2, 0), (4, 0)])

        board.remove_tile(3, 1)
        board.remove_tile(2, 0)
        spaces = board.reachable_spaces(0, 0)
        self.assertTrue(spaces == [(1, 0), (2, 1)])



if __name__ == '__main__':
    unittest.main()