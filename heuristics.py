from cst import *  
from utils import *  

"""
    Heuristic function that counts the number of non-BLACK cells in the grid.
    
    Args:
        grid (list): A 2D list representing the current state of the grid.
    
    Returns:
        int: The number of cells that are not BLACK (i.e., filled cells).
    """
def heuristic_filled_cells(grid):
    return sum(cell != BLACK for row in grid for cell in row)

"""
    Heuristic function that counts the number of remaining blocks.
    
    Args:
        blocks (list): A list of tuples representing the remaining blocks and their colors.
    
    Returns:
        int: The number of remaining blocks.
    """
def heuristic_remaining_blocks(blocks):
    return len(blocks)

"""
    A combined heuristic function that evaluates the grid and blocks.
    It penalizes filled cells but rewards potential line clears and remaining blocks.
    
    Args:
        grid (list): A 2D list representing the current state of the grid.
        blocks (list): A list of tuples representing the remaining blocks and their colors.
    
    Returns:
        int: A heuristic score for the current state.
    """
def combined_heuristic(grid, blocks):
    filled = sum(cell != BLACK for row in grid for cell in row) # Count the number of filled cells (non-BLACK cells)
    
    # Count the number of lines (rows or columns) that can be cleared in the next move
    lines = 0
    for i in range(len(grid)):
        if all(cell != BLACK for cell in grid[i]):  # Check if a row can be cleared
            lines += 1
    for j in range(len(grid[0])):
        if all(grid[i][j] != BLACK for i in range(len(grid))):  # Check if a column can be cleared
            lines += 1
    
    # Calculate the heuristic score:
    # - Penalize filled cells (higher filled = worse)
    # - Reward potential line clears (each line reduces the score by 10)
    # - Reward remaining blocks (more blocks = higher score, multiplied by 5) 
    return filled - (lines * 10) + len(blocks) * 5

"""
    Heuristic function that evaluates how many blocks can be removed from the grid.
    
    Args:
        grid (list): A 2D list representing the current state of the grid.
        blocks (list): A list of tuples representing the remaining blocks and their colors.
    
    Returns:
        int: A heuristic score based on the number of removable blocks (negative value to prioritize states with fewer removable blocks).
    """
def heuristic_block_removal(grid, blocks):
    removable_blocks = 0  # Counter for removable blocks
    
    # Iterate over each block and its color
    for block, color in blocks:
        # Get all possible rotations of the block
        for rotation in get_rotations(block):
            # Try to place the block at every possible position on the grid
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    # Check if the block can be placed at the current position
                    if can_place_block(rotation, x, y, grid):
                        removable_blocks += 1  # Increment the counter if the block can be placed
                        break  # Move to the next block
                else:
                    continue  # Continue to the next position if the block cannot be placed
                break  # Exit the loop if the block can be placed
                
    return -removable_blocks # Return a negative value to prioritize states with fewer removable blocks