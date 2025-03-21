from cst import *
from utils import *

def heuristic_filled_cells(grid):
    return sum(cell != BLACK for row in grid for cell in row)

def heuristic_remaining_blocks(blocks):
    return len(blocks)

def combined_heuristic_empty_grid(grid):
    filled_cells = sum(cell != BLACK for row in grid for cell in row)
    remaining_blocks = len([block for block in grid if block != BLACK])  # Adjust this as needed
    return filled_cells + remaining_blocks

def heuristic_block_removal(grid, blocks):
    removable_blocks = 0
    for block, color in blocks:
        for rotation in get_rotations(block):
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid):
                        removable_blocks += 1
                        break
                else:
                    continue
                break
    return -removable_blocks
