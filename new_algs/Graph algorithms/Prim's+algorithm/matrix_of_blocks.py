# imports
from blocks.background_block import Background
from blocks.wall_block import Wall
from blocks.abstract_block import AbtractBlock
from general.consts_values import Blocks
from typing import List


# matrix class - 2-dimensional list used to represent level
class Matrix(object):
    # constructor - initializes two dimensional matrix / table
    def __init__(self, number_of_columns: int, number_of_rows: int):
        self.columns: int = number_of_columns
        self.rows: int = number_of_rows
        self.two_dim_list: List[List[AbtractBlock]] = [[None for x in range(self.rows)] for y in range(self.columns)]

    # setting particular block in two dimensional list (matrix) into Background
    def set_block_to_background(self, pos_x: int, pos_y: int):
        if 0 <= pos_x <= self.columns - 1 and 0 <= pos_y <= self.rows - 1:
            self.two_dim_list[pos_x][pos_y] = Background(pos_x, pos_y)

    # setting particular block in two dimensional list (matrix) into Wall
    # noinspection PyTypeChecker
    def set_block_to_wall(self, pos_x: int, pos_y: int):
        if 0 <= pos_x <= self.columns - 1 and 0 <= pos_y <= self.rows - 1:
            self.two_dim_list[pos_x][pos_y] = Wall(pos_x, pos_y)

    # changes particular block's type in two dimensional list (matrix)
    # noinspection PyTypeChecker
    def change_blocks_type(self, pos_x: int, pos_y: int, new_blocks_type: str):
        # if block is not in the matrix, then do not execute rest of the method
        if pos_x < 0 or pos_x > self.columns - 1 or pos_y < 0 or pos_y > self.rows - 1:
            return
        if new_blocks_type == Blocks.BACKGROUND:
            self.two_dim_list[pos_x][pos_y] = Background(pos_x, pos_y)
        elif new_blocks_type == Blocks.WALL:
            self.two_dim_list[pos_x][pos_y] = Wall(pos_x, pos_y)

    # checks if it is possible to move into that block
    def check(self, pos_x: int, pos_y: int) -> bool:
        if pos_x < 0 or pos_x >= self.columns or pos_y < 0 or pos_y >= self.rows:
            return False
        else:
            return bool(self.two_dim_list[pos_x][pos_y])

    # checks blocks type (if block is available)
    def checks_blocks_type(self, pos_x: int, pos_y: int) -> str:
        if pos_x < 0 or pos_x >= self.columns or pos_y < 0 or pos_y >= self.rows:
            return "none"
        return self.two_dim_list[pos_x][pos_y].block_type
