from tkinter import *
import random
from enum import Enum
from copy import deepcopy


# Enum to represent the state of each tile. REALTILE means that it is a tile that has not been stepped on. Hole means
# that this tile has been removed from the board.
class Tile_State(Enum):
    HOLE = 0
    TILE = 1
    PLAYER = 2


# Class that represents a tile. A tile contains a fish variable tracking the number of fish on that tile, and a state
# variable tracking the current state of the tile (is it a hole, or available to consume)
class Tile:
    def __init__(self, state: Tile_State, num_fish: int):
        self.fish = num_fish
        self.state = state
        if state == Tile_State.HOLE:
            self.fish = 0

    @staticmethod
    def create_tile(fish: int):
        return Tile(Tile_State.TILE, fish)

    @staticmethod
    def create_hole():
        return Tile(Tile_State.HOLE, 0)

    @staticmethod
    def create_player_tile(fish: int):
        return Tile(Tile_State.PLAYER, fish)

    # Draws the hexagons for each space, followed by the fish in each hexagon
    def draw (self, window, x_coord, y_coord, size):
        penguin_size = size / 5
        if self.state == Tile_State.TILE or self.state == Tile_State.PLAYER:
            window.create_polygon(x_coord, y_coord + size,
                                  x_coord + size, y_coord,
                                  x_coord + size * 2, y_coord,
                                  x_coord + size * 3, y_coord + size,
                                  x_coord + size * 2, y_coord + size * 2,
                                  x_coord + size, y_coord + size * 2,
                                  fill = "orange",
                                  outline = "black")  #Fill white
            offset = .3 * size
            cur_offset = offset * (self.fish / 2) - (offset * .5) - (penguin_size / 2) + size
            for i in range(self.fish):
              
                self.draw_fish(window = window,
                               x_coord = x_coord + size*1.3,
                               y_coord = y_coord+ cur_offset,
                               size = penguin_size)
                cur_offset -= offset

    # Draws a fish
    @staticmethod
    def draw_fish(window, x_coord, y_coord, size):
        window.create_polygon(x_coord, y_coord,
                              x_coord, y_coord + size,
                              x_coord + size/2, y_coord,
                              x_coord + 3 * size /2, y_coord,
                              x_coord + 2 * size, y_coord + size /2,
                              x_coord + 3 * size / 2, y_coord + size,
                              x_coord + size /2, y_coord + size,
                              fill="dodger blue")

    # Sets the state of the tile to hole, indicating that it cannot be stepped on. Also sets fish to 0.
    def remove_tile(self):
        self.state = Tile_State.HOLE
        self.fish = 0

    def set_player(self):
        self.state = Tile_State.PLAYER

    def remove_penguin(self):
        self.state = Tile_State.TILE

    def get_fish(self):
        return self.fish

    def get_state(self):
        return self.state

    def valid_tile(self):
        return self.state == Tile_State.TILE

    def __str__(self):
        if self.get_state() == Tile_State.PLAYER:
            return "-1"
        return str(self.fish)


# Class representing the board, which containing a NxM grid of Tiles, and an integer field "count_ones" which tracks the
# number of tiles in the grid that contain one fish. This is useful for ensuring that the board adheres to the provided
# minimum number of tiles that must contain one fish.

# The coordinate system for a board is represented as grid of hexagons with points (x,y), where x is the row number and y is the column number.  A 3x3 board is visualized as follows:
'''
        _____                   _____                   _____
    /   (0,0)   \   _____   /   (0,1)   \   _____   /   (0,2)   \   _____
    \   _____   /   (1,0)   \   _____   /   (1,1)   \   _____   /   (1,2)   \
    /   (2,0)   \   _____   /   (2,1)   \   _____   /   (2,2)   \   _____   /
    \   _____   /           \   _____   /           \   _____   /


'''


class Board:
    """
    __init__: Constructs a board from a 2-D list of integers, with each integer representing a tile containing the
              corresponding number of fish.
    Params:
        tiles: A 2-D list of integers representing fishes on tiles.
    """
    def __init__(self, tiles: list):
        self.board = []
        for row in range(len(tiles)):
            curr_row = []
            for column in range(len(tiles[row])):
                if tiles[row][column] == 0:
                    curr_row.append(Tile.create_hole())
                else:
                    curr_row.append(Tile.create_tile(tiles[row][column]))
            self.board.append(curr_row)

    @staticmethod
    def make_random_board(rows:int, columns: int, holes=None, min_ones=0):
        """
        make_random_board: Static constructor that constructs a full board of given width and height with tiles
                           containing random numbers of fish. Allows the caller to specify that certain spaces
                           should be holes, and also allows the caller to specify a minimum number of tiles that
                           contain exactly 1 fish.

        Params:
            height: height of the board
            width: width of the board
            holes (optional): list of tuples containing the coordinates at which holes are to be created.
            min_ones (optional): int representing the minimum number of tiles that have exactly 1 fish.

        Output -> Board
        """
        # Creates a random board
        if holes is None:
            holes = []
        tiles = []
        for i in range(rows):
            row = []
            for j in range(columns):
                fish = random.randint(1, 5)
                row.append(fish)
            tiles.append(row)
        # Turns the tiles at the specified coordinates into holes
        for row, column in holes:
            tiles[row][column] = 0
        min_ones_tiles = []
        for i in range(min_ones):
            row = random.randint(0, rows - 1)
            column = random.randint(0, columns - 1)
            while (row, column) in min_ones_tiles:
                row = random.randint(0, rows - 1)
                column = random.randint(0, columns - 1)
            min_ones_tiles.append((row, column))
        for row, column in min_ones_tiles:
            tiles[row][column] = 1
        return Board(tiles)

    @staticmethod
    def make_uniform_board(rows: int, columns: int, fish: int):
        """
        make_uniform_board: Static constructor that takes a width, height, and fish argument and returns a board with the
                            specified width and height, with each tile in the board containing the specified number of fish.
        Params:
            width: width of board
            height: height of board
            fish: number of fish on each tile

        Output -> Board
        """
        tiles = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(fish)
            tiles.append(row)
        return Board(tiles)

    @staticmethod
    def make_board_from_tiles(tiles: list):
        """
        make_board_from_tiles: Static constructor that takes a list of list of integers representing the tiles of the board
                               and constructs a board.
        Params:
            tiles: list of list of integers representing each tile in the board.

        Output -> Board
        """
        return Board(tiles)

    # Takes the provided coordinates of holes and removes those tiles from play.
    def remove_holes(self, holes):
        for i in holes:
            row, column = i
            self.remove_tile(row,column)

    def remove_tile(self, row: int, column: int):
        """
        remove_tile: Changes the tile at the specified x and y coordinate to be a hole. This method is idempotent (can be
                     called repeatedly with no change after the first invocation).
        Params:
            x_coord: x coordinate of tile
            y_coord: y coordinate of tile
        """
        self.board[row][column].remove_tile()

    def place_player(self, location: tuple):
        self.board[location[0]][location[1]].set_player()

    def remove_penguin(self, location: tuple):
        self.board[location[0]][location[1]].remove_penguin()

    def place_players(self, coordinates: list):
        for row, column in coordinates:
            self.place_player((row, column))

    # Draws the board
    def draw(self, window, size):
        for i in range(len(self.board[0])):
            everyother = False
            for j in range(len(self.board)):
                offset_x = i * size * 4
                offset_y = j * size
                if everyother:
                    offset_x = offset_x + 2 * size
                everyother =  not everyother

                self.board[j][i].draw(window, offset_x, offset_y, size)
        
     #   for i in range(0, len(self.board))

    # ## Returns a list of points that a player can move to from the provided x and y coordinates, without going through other players
    # ## The location of other players is provided as a list of tuples containing the x and y coordinate of the other players.
    # def movable_spaces(self, x_coord: int, y_coord: int, players: dict):
    #     penguins = []
    #     for _, player in players.items():
    #         for loc in player.penguin_locations:
    #             penguins.append(loc)
    #     spaces = []
    #     space_y_greater = len(self.board) - y_coord - 1
    #     space_y_less = y_coord
    #     x = 0
    #     y = 0
    #     for i in range(space_y_greater):
    #         y = y + 2
    #         if self.check_valid_tile(x_coord + x, y_coord + y) and not [x_coord + x, y_coord + y] in penguins:
    #             spaces.append((x_coord + x, y_coord + y))
    #         else:
    #             break
    #     x = 0
    #     y = 0
    #     for i in range(space_y_less):
    #         y = y - 2
    #         if self.check_valid_tile(x_coord + x, y_coord + y) and not [x_coord + x, y_coord + y] in penguins:
    #             spaces.append((x_coord + x, y_coord + y))
    #         else:
    #             break
    #
    #     x = 0
    #     y = 0
    #     for i in range(space_y_greater * 2):
    #         y = y + 1
    #         if (y_coord + y) % 2 == 0:
    #             x = x + 1
    #         if self.check_valid_tile(x_coord + x, y_coord + y) and not [x_coord + x, y_coord + y] in penguins:
    #             spaces.append((x_coord + x, y_coord + y))
    #         else:
    #             break
    #
    #     x = 0
    #     y = 0
    #     for i in range(space_y_greater * 2):
    #         y = y + 1
    #         if (y_coord + y) % 2 != 0:
    #             x = x - 1
    #         if self.check_valid_tile(x_coord + x, y_coord + y) and not [x_coord + x, y_coord + y] in penguins:
    #             spaces.append((x_coord + x, y_coord + y))
    #         else:
    #             break
    #
    #     x = 0
    #     y = 0
    #     for i in range(space_y_less * 2):
    #         y = y - 1
    #         if (y_coord + y) % 2 == 0:
    #             x = x + 1
    #         if self.check_valid_tile(x_coord + x, y_coord + y) and not [x_coord + x, y_coord + y] in penguins:
    #             spaces.append((x_coord + x, y_coord + y))
    #         else:
    #             break
    #
    #     x = 0
    #     y = 0
    #     for i in range(space_y_less * 2):
    #         y = y - 1
    #         if (y_coord + y) % 2 != 0:
    #             x = x - 1
    #         if self.check_valid_tile(x_coord + x, y_coord + y) and not [x_coord + x, y_coord + y] in penguins:
    #             spaces.append((x_coord + x, y_coord + y))
    #         else:
    #             break
    #     return spaces

    def reachable_spaces(self, row: int, column: int, depth=float("inf")):
        moves = []
        moves.extend(self.reachable_spaces_north(row, column, depth=depth))
        moves.extend(self.reachable_spaces_northeast(row, column, depth=depth))
        moves.extend(self.reachable_spaces_southeast(row, column, depth=depth))
        moves.extend(self.reachable_spaces_south(row, column, depth=depth))
        moves.extend(self.reachable_spaces_southwest(row, column, depth=depth))
        moves.extend(self.reachable_spaces_northwest(row, column, depth=depth))
        return moves

    def reachable_spaces_north(self, row: int, column: int, depth=float("inf")):
        spaces = []
        row_idx = row - 2
        while(self.valid_row(row_idx)
              and self.board[row_idx][column].valid_tile()
              and depth > 0):
            spaces.append((row_idx, column))
            row_idx = row_idx - 2
            depth = depth - 1
        return spaces

    def reachable_spaces_south(self, row: int, column: int, depth=float("inf")):
        spaces = []
        row_idx = row + 2
        while(self.valid_row(row_idx)
              and self.board[row_idx][column].valid_tile()
              and depth > 0):
            spaces.append((row_idx, column))
            row_idx = row_idx + 2
            depth = depth - 1
        return spaces

    def reachable_spaces_northeast(self, row: int, column: int, depth=float("inf")):
        spaces = []
        row_idx = row
        column_idx = column
        if row_idx % 2 == 0:
            row_idx = row_idx - 1

        else:
            row_idx = row_idx - 1
            column_idx = column_idx + 1
        while(self.valid_row(row_idx)
              and self.valid_column(column_idx)
              and self.board[row_idx][column_idx].valid_tile()
              and depth > 0):
            spaces.append((row_idx, column_idx))
            if row_idx % 2 == 0:
                row_idx = row_idx - 1
            else:
                row_idx = row_idx - 1
                column_idx = column_idx + 1
            depth = depth - 1
        return spaces

    def reachable_spaces_southeast(self, row: int, column: int, depth=float("inf")):
        spaces = []
        row_idx = row
        column_idx = column
        if row_idx % 2 == 0:
            row_idx = row_idx + 1

        else:
            row_idx = row_idx + 1
            column_idx = column_idx + 1
        while(self.valid_row(row_idx)
              and self.valid_column(column_idx)
              and self.board[row_idx][column_idx].valid_tile()
              and depth > 0):
            spaces.append((row_idx, column_idx))
            if row_idx % 2 == 0:
                row_idx = row_idx + 1
            else:
                row_idx = row_idx + 1
                column_idx = column_idx + 1
            depth = depth - 1
        return spaces

    def reachable_spaces_northwest(self, row: int, column: int, depth=float("inf")):
        spaces = []
        row_idx = row
        column_idx = column
        if row_idx % 2 == 0:
            row_idx = row_idx - 1
            column_idx = column_idx - 1
        else:
            row_idx = row_idx - 1
        while(self.valid_row(row_idx)
              and self.valid_column(column_idx)
              and self.board[row_idx][column_idx].valid_tile()
              and depth > 0):
            spaces.append((row_idx, column_idx))
            if row_idx % 2 == 0:
                row_idx = row_idx - 1
                column_idx = column_idx - 1
            else:
                row_idx = row_idx - 1
            depth = depth - 1
        return spaces

    def reachable_spaces_southwest(self, row: int, column: int, depth=float("inf")):
        spaces = []
        row_idx = row
        column_idx = column
        if row_idx % 2 == 0:
            row_idx = row_idx + 1
            column_idx = column_idx - 1
        else:
            row_idx = row_idx + 1
        while(self.valid_row(row_idx)
              and self.valid_column(column_idx)
              and self.board[row_idx][column_idx].valid_tile()
              and depth > 0):
            spaces.append((row_idx, column_idx))
            if row_idx % 2 == 0:
                row_idx = row_idx + 1
                column_idx = column_idx - 1
            else:
                row_idx = row_idx + 1
            depth = depth - 1
        return spaces

    def valid_row(self, row: int):
        return 0 <= row < len(self.board)

    def valid_column(self, column: int):
        return 0 <= column < len(self.board[0])

    def check_valid_tile(self, row_coord : int, column_coord : int):
        """
        check_valid_tile: returns True if the tile at the provided coordinates is a REALTILE; else returns False.

        Params:
            x_coord: x coordinate of tile
            y_coord: y coordinate of tile

        Output -> Boolean
        """
        if not self.valid_row(row_coord) or not self.valid_column(column_coord):
            return False
        return self.board[row_coord][column_coord].valid_tile()

    def get_board(self):
        """
        get_board: returns a list of list of integers, with each tile representing the number of fish on that tile.
                   0 indicates that the tile is a hole.
        Output -> List of List of ints
        """
        int_board = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[i])):
                row.append(self.board[i][j].get_fish())
            int_board.append(row)
        return int_board

    def get_board_str(self):
        board = self.get_board()
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].get_state() == Tile_State.PLAYER:
                    board[i][j] = float("inf")
        return board

    def get_board_size(self):
        return len(self.board), len(self.board[0])

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return self.get_board() == other.get_board()

    def __hash__(self):
        return hash(self.get_board())
