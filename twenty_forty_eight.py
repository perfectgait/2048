"""
Clone of 2048 game.
"""

# import poc_2048_gui
import poc_simpletest
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    merged_line = []
    previous_number = 0
    merged_indexes = []

    for number in line:
        index_to_update = len(merged_line) - 1

        if previous_number > 0 and previous_number == number and index_to_update not in merged_indexes:
            merged_line[index_to_update] = previous_number * 2
            previous_number = previous_number * 2
            merged_indexes.append(index_to_update)
        elif number > 0:
            merged_line.append(number)
            previous_number = number

    if len(merged_line) < len(line):
        merged_line += [0] * (len(line) - len(merged_line))

    return merged_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Initialize the game
        """
        self._board = []
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_cells = {
            UP: [(0, col) for col in range(0, self._grid_width)],
            DOWN: [(self._grid_height - 1, col) for col in range(0, self._grid_width)],
            LEFT: [(row, 0) for row in range(0, self._grid_height)],
            RIGHT: [(row, self._grid_width - 1) for row in range(0, self._grid_height)]
        }

        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two initial tiles.
        """
        self._board = [[0 for dummy_col in range(0, self._grid_width)] for dummy_row in range(0, self._grid_height)]

        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        board_as_string = ""

        for row in self._board:
            board_as_string += str(row).strip('[]') + "\n"

        return board_as_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add a new tile if any tiles moved.
        """
        has_changes = False

        for initial_row, initial_col in self._initial_cells[direction]:
            line = [self.get_tile(initial_row, initial_col)]

            if direction == UP or direction == DOWN:
                num_steps = self._grid_height
            else:
                num_steps = self._grid_width

            for step in range(1, num_steps):
                row = initial_row + step * OFFSETS[direction][0]
                col = initial_col + step * OFFSETS[direction][1]
                line.append(self.get_tile(row, col))

            merged_line = merge(line)

            self.set_tile(initial_row, initial_col, merged_line[0])

            for index, value in enumerate(merged_line):
                if line[index] != value:
                    has_changes = True

                row = initial_row + index * OFFSETS[direction][0]
                col = initial_col + index * OFFSETS[direction][1]

                self.set_tile(row, col, value)

        if has_changes:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty square.  The tile should be 2 90% of the time and 4 10% of the
        time.
        """
        random_value = random.random()
        random_tile = self.find_random_empty_tile()

        if random_tile is None:
            return

        if random_value <= .9:
            new_tile_value = 2
        else:
            new_tile_value = 4

        self.set_tile(random_tile[0], random_tile[1], new_tile_value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]

    def find_random_empty_tile(self):
        """
        Find an empty tile in the board at random
        """
        empty_tiles = []

        for row_index, row in enumerate(self._board):
            for col_index, dummy_col in enumerate(row):
                if self.get_tile(row_index, col_index) == 0:
                    empty_tiles.append((row_index, col_index))

        if len(empty_tiles) <= 0:
            return None

        return random.choice(empty_tiles)


def test_merge():
    """
    Test code for merge
    """
    suite = poc_simpletest.TestSuite()

    suite.run_test(merge([2, 0, 2, 4]), [4, 4, 0, 0])
    suite.run_test(merge([0, 0, 2, 2]), [4, 0, 0, 0])
    suite.run_test(merge([2, 2, 0, 0]), [4, 0, 0, 0])
    suite.run_test(merge([2, 2, 2, 2, 2]), [4, 4, 2, 0, 0])
    suite.run_test(merge([8, 16, 16, 8]), [8, 32, 8, 0])

    suite.report_results()

def test_twenty_forty_eight():
    """
    Test code for TwentyFortyEight
    """
    suite = poc_simpletest.TestSuite()

    twenty_forty_eight = TwentyFortyEight(4, 6)

    suite.run_test(twenty_forty_eight.get_grid_height(), 4)

    suite.run_test(twenty_forty_eight.get_grid_width(), 6)

    twenty_forty_eight.set_tile(1, 1, 5)
    suite.run_test(twenty_forty_eight.get_tile(1, 1), 5)
    twenty_forty_eight.set_tile(0, 0, 10)
    suite.run_test(twenty_forty_eight.get_tile(0, 0), 10)
    twenty_forty_eight.set_tile(3, 5, 7)
    suite.run_test(twenty_forty_eight.get_tile(3, 5), 7)

    small_twenty_forty_eight = TwentyFortyEight(2, 2)

    small_twenty_forty_eight.set_tile(0, 0, 2)
    small_twenty_forty_eight.set_tile(0, 1, 2)
    small_twenty_forty_eight.set_tile(1, 0, 4)
    small_twenty_forty_eight.set_tile(1, 1, 0)

    expected_random_empty_tile = 1, 1
    suite.run_test(small_twenty_forty_eight.find_random_empty_tile(), expected_random_empty_tile)

    small_twenty_forty_eight.set_tile(1, 1, 4)
    expected_random_empty_tile = None
    suite.run_test(small_twenty_forty_eight.find_random_empty_tile(), expected_random_empty_tile)

    move_up_twenty_forty_eight = TwentyFortyEight(4, 4)
    move_up_twenty_forty_eight.set_tile(0, 0, 4)
    move_up_twenty_forty_eight.set_tile(0, 1, 2)
    move_up_twenty_forty_eight.set_tile(0, 2, 2)
    move_up_twenty_forty_eight.set_tile(0, 3, 2)
    move_up_twenty_forty_eight.set_tile(1, 0, 0)
    move_up_twenty_forty_eight.set_tile(1, 1, 0)
    move_up_twenty_forty_eight.set_tile(1, 2, 2)
    move_up_twenty_forty_eight.set_tile(1, 3, 8)
    move_up_twenty_forty_eight.set_tile(2, 0, 4)
    move_up_twenty_forty_eight.set_tile(2, 1, 2)
    move_up_twenty_forty_eight.set_tile(2, 2, 2)
    move_up_twenty_forty_eight.set_tile(2, 3, 8)
    move_up_twenty_forty_eight.set_tile(3, 0, 0)
    move_up_twenty_forty_eight.set_tile(3, 1, 2)
    move_up_twenty_forty_eight.set_tile(3, 2, 0)
    move_up_twenty_forty_eight.set_tile(3, 3, 4)

    move_up_twenty_forty_eight.move(UP)

    suite.run_test(move_up_twenty_forty_eight.get_tile(0, 0), 8)
    suite.run_test(move_up_twenty_forty_eight.get_tile(0, 1), 4)
    suite.run_test(move_up_twenty_forty_eight.get_tile(0, 2), 4)
    suite.run_test(move_up_twenty_forty_eight.get_tile(0, 3), 2)
    suite.run_test(move_up_twenty_forty_eight.get_tile(1, 1), 2)
    suite.run_test(move_up_twenty_forty_eight.get_tile(1, 2), 2)
    suite.run_test(move_up_twenty_forty_eight.get_tile(1, 3), 16)
    suite.run_test(move_up_twenty_forty_eight.get_tile(2, 3), 4)

    move_right_twenty_forty_eight = TwentyFortyEight(4, 5)

    move_right_twenty_forty_eight.set_tile(0, 0, 8)
    move_right_twenty_forty_eight.set_tile(0, 1, 16)
    move_right_twenty_forty_eight.set_tile(0, 2, 8)
    move_right_twenty_forty_eight.set_tile(0, 3, 16)
    move_right_twenty_forty_eight.set_tile(0, 4, 8)
    move_right_twenty_forty_eight.set_tile(1, 0, 16)
    move_right_twenty_forty_eight.set_tile(1, 1, 8)
    move_right_twenty_forty_eight.set_tile(1, 2, 16)
    move_right_twenty_forty_eight.set_tile(1, 3, 8)
    move_right_twenty_forty_eight.set_tile(1, 4, 16)
    move_right_twenty_forty_eight.set_tile(2, 0, 8)
    move_right_twenty_forty_eight.set_tile(2, 1, 16)
    move_right_twenty_forty_eight.set_tile(2, 2, 8)
    move_right_twenty_forty_eight.set_tile(2, 3, 16)
    move_right_twenty_forty_eight.set_tile(2, 4, 8)
    move_right_twenty_forty_eight.set_tile(3, 0, 16)
    move_right_twenty_forty_eight.set_tile(3, 1, 8)
    move_right_twenty_forty_eight.set_tile(3, 2, 16)
    move_right_twenty_forty_eight.set_tile(3, 3, 8)
    move_right_twenty_forty_eight.set_tile(3, 4, 16)

    move_right_twenty_forty_eight.move(RIGHT)

    suite.run_test(move_right_twenty_forty_eight.get_tile(0, 0), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(0, 1), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(0, 2), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(0, 3), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(0, 4), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(1, 0), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(1, 1), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(1, 2), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(1, 3), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(1, 4), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(2, 0), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(2, 1), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(2, 2), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(2, 3), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(2, 4), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(3, 0), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(3, 1), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(3, 2), 16)
    suite.run_test(move_right_twenty_forty_eight.get_tile(3, 3), 8)
    suite.run_test(move_right_twenty_forty_eight.get_tile(3, 4), 16)

    suite.report_results()


test_merge()
test_twenty_forty_eight()

# poc_2048_gui.run_gui(TwentyFortyEight(4, 4))