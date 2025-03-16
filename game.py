from cst import GRID_SIZE, BLACK, SHAPES, COLORS
from heuristics import heuristic_empty_cells
import random 

# Generate a random block
def generate_block():
    return random.choice(SHAPES), random.choice(COLORS)

# State representation
class State:
    def __init__(self, grid, blocks, moves=0):
        self.grid = grid
        self.blocks = blocks
        self.moves = moves

    def is_goal(self):
        return all(cell != BLACK for row in self.grid for cell in row)

    def get_successors(self):
        successors = []
        for block, color in self.blocks:
            for rotation in get_rotations(block):
                for x in range(GRID_SIZE):
                    for y in range(GRID_SIZE):
                        if can_place_block(rotation, x, y, self.grid):
                            new_grid = [row[:] for row in self.grid]
                            place_block(rotation, x, y, color, new_grid)
                            new_blocks = self.blocks.copy()
                            new_blocks.remove((block, color))
                            successors.append(State(new_grid, new_blocks, self.moves + 1))
        return successors

    def __lt__(self, other):
        return heuristic_empty_cells(self.grid) < heuristic_empty_cells(other.grid)

# Helper functions
def get_rotations(block):
    rotations = [block]
    for _ in range(3):
        block = list(zip(*block[::-1]))
        rotations.append(block)
    return rotations

def can_place_block(block, x, y, grid):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                if x + col < 0 or x + col >= GRID_SIZE or y + row >= GRID_SIZE or grid[y + row][x + col] != BLACK:
                    return False
    return True

def place_block(block, x, y, color, grid):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                grid[y + row][x + col] = color