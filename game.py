# game.py
from cst import *
from heuristics import heuristic_filled_cells
import random
from utils import *

# Generate a random block
def generate_block(level):
    return random.choice(LEVEL_BLOCKS[level])

# State representation
class State:
    def __init__(self, grid, blocks, moves=0):
        self.grid = grid
        self.blocks = blocks
        self.moves = moves

    def is_goal(self):
        return all(cell == BLACK for row in self.grid for cell in row)

    def get_successors(self, level):
        successors = []
        if not self.blocks:
            print("No blocks left!")
            return successors
        for block, color in self.blocks:
            for x in range(GRID_SIZE - len(block) + 1):
                for y in range(GRID_SIZE - len(block[0]) + 1):
                    if can_place_block(block, x, y, self.grid, GRID_SIZE):
                        new_grid = [row[:] for row in self.grid]
                        place_block(block, x, y, color, new_grid, GRID_SIZE)
                        new_blocks = self.blocks.copy()
                        new_blocks.remove((block, color))
                        successors.append(State(new_grid, new_blocks, self.moves + 1))
        return successors

    def __hash__(self):
        grid_tuple = tuple(map(tuple, self.grid))
        blocks_tuple = tuple((tuple(map(tuple, block)), color) for block, color in self.blocks)
        return hash((grid_tuple, blocks_tuple))

    def __eq__(self, other):
        return self.grid == other.grid and self.blocks == other.blocks

    def __lt__(self, other):
        return heuristic_filled_cells(self.grid) < heuristic_filled_cells(other.grid)