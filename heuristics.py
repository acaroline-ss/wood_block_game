from cst import *
from utils import *

def heuristic_filled_cells(grid, blocks=None):
    """
    Counts the number of non-empty (filled) cells in the grid.
    
    This simple heuristic evaluates the current state by counting how many cells
    are occupied. Lower values indicate better states (less filled cells).
    
    Args:
        grid (list[list]): 2D array representing the game grid
        blocks (list, optional): Unused parameter kept for interface consistency
        
    Returns:
        int: Count of non-BLACK cells in the grid
    """
    return sum(cell != BLACK for row in grid for cell in row)

def heuristic_remaining_blocks(grid, blocks):
    """
    Evaluates state based on number of remaining blocks.
    
    This heuristic prioritizes states with fewer remaining blocks to place.
    The assumption is that fewer remaining blocks means we're closer to solving.
    
    Args:
        grid (list[list]): 2D array representing the game grid (unused)
        blocks (list): List of remaining block objects to place
        
    Returns:
        int: Count of remaining blocks
    """
    return len(blocks)

def combined_heuristic(grid, blocks):
    """
    Comprehensive heuristic combining multiple game state factors.
    
    Evaluates the state by considering:
    1. Penalty for filled cells
    2. Bonus for potential line clears
    3. Bonus for remaining blocks (as having options is good)
    
    Args:
        grid (list[list]): 2D array representing the game grid
        blocks (list): List of remaining block objects
        
    Returns:
        int: Combined heuristic score (lower is better)
    """
    # Count filled cells (non-BLACK cells)
    filled = sum(cell != BLACK for row in grid for cell in row)
    
    # Count clearable lines (rows/columns with no empty cells)
    lines = 0
    grid_size = len(grid)
    
    # Check all rows and columns for potential clears
    lines += sum(all(cell != BLACK for cell in row) for row in grid)
    lines += sum(all(grid[i][j] != BLACK for i in range(grid_size)) 
                for j in range(len(grid[0])))
    
    # Weighted components:
    # - Filled cells are bad (positive weight)
    # - Clearable lines are good (negative weight)
    # - More remaining blocks is good (negative weight)
    return filled - (lines * 10) + len(blocks) * 5

def heuristic_block_removal(grid, blocks):
    """
    Evaluates how many blocks could potentially be removed from the current state.
    
    This heuristic counts how many of the remaining blocks could be placed
    in the current grid configuration. Returns a negative value because
    fewer removable blocks is better (means we've placed more blocks).
    
    Args:
        grid (list[list]): 2D array representing the game grid
        blocks (list): List of remaining (block, color) tuples
        
    Returns:
        int: Negative count of removable blocks (lower is better)
    """
    removable_blocks = 0
    
    for block, color in blocks:
        # Check if any rotation of the block can be placed anywhere
        for rotation in get_rotations(block):
            # Using generator expression for early termination
            if any(can_place_block(rotation, x, y, grid)
                  for x in range(GRID_SIZE)
                  for y in range(GRID_SIZE)):
                removable_blocks += 1
                break  # No need to check other positions if we found one
    
    return -removable_blocks