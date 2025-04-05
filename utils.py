from cst import *
import random

def get_rotations(block):
    """
    Generates all unique 90-degree rotations of a block.
    
    For each rotation, we transpose and reverse rows to achieve 90° rotation.
    This is more efficient than checking all 4 rotations when blocks have symmetry.
    
    Args:
        block (list[list]): 2D matrix representing the block (1=filled, 0=empty)
        
    Returns:
        list[list[list]]: List of unique rotated versions of the block
    """
    rotations = [block]
    current = block
    
    # Only need to rotate 3 times to get all 4 possible orientations
    for _ in range(3):
        # Rotate 90° clockwise by transposing and reversing each row
        current = [list(row)[::-1] for row in zip(*current)]
        if not any(are_blocks_equal(current, rot) for rot in rotations):
            rotations.append(current)
            
    return rotations

def can_place_block(block, x, y, grid, GRID_SIZE, tolerance=None):
    """
    Checks if a block can be placed at (x,y) on the grid without overlaps or out-of-bounds.
    
    Args:
        block (list[list]): 2D block matrix to place
        x,y (int): Top-left grid coordinates for placement
        grid (list[list]): Current game grid state
        GRID_SIZE (int): Dimensions of the grid
        tolerance (int, optional): Unused parameter kept for compatibility
        
    Returns:
        bool: True if placement is valid, False otherwise
    """
    block_height, block_width = len(block), len(block[0])
    
    # First check if block would be out of bounds
    if x < 0 or y < 0 or x + block_width > GRID_SIZE or y + block_height > GRID_SIZE:
        return False
        
    # Check each cell in the block against grid
    for dy, row in enumerate(block):
        for dx, cell in enumerate(row):
            if cell and grid[y + dy][x + dx] != BLACK:
                return False
                
    return True

def place_block(block, x, y, color, grid, GRID_SIZE):
    """
    Places a block on the grid at specified position with given color.
    
    Modifies the grid in-place. Assumes placement has already been validated.
    
    Args:
        block (list[list]): Block to place
        x,y (int): Top-left grid coordinates
        color (tuple): RGB color for the block
        grid (list[list]): Grid to modify
        GRID_SIZE (int): For bounds checking (debug purposes)
    """
    for dy, row in enumerate(block):
        for dx, cell in enumerate(row):
            if cell:
                # Assert we're not overwriting existing blocks
                assert grid[y + dy][x + dx] == BLACK, "Overwriting existing block!"
                grid[y + dy][x + dx] = color

def no_valid_moves_left(grid, blocks, GRID_SIZE):
    """
    Determines if there are no remaining valid placements for any blocks.
    
    Optimized by checking rotations first and using early termination.
    
    Args:
        grid (list[list]): Current game state
        blocks (list[tuple]): List of (block, color) remaining
        GRID_SIZE (int): Grid dimensions
        
    Returns:
        bool: True if no valid moves remain
    """
    for block, _ in blocks:
        # Check all unique rotations first
        for rotation in get_rotations(block):
            # Check all possible positions
            for y in range(GRID_SIZE - len(rotation) + 1):
                for x in range(GRID_SIZE - len(rotation[0]) + 1):
                    if can_place_block(rotation, x, y, grid, GRID_SIZE):
                        return False
    return True

def clear_completed_lines(grid, GRID_SIZE):
    """
    Clears any fully filled rows or columns and returns count of cleared lines.
    
    More efficient implementation that tracks lines first then clears them.
    
    Args:
        grid (list[list]): Grid to check and modify
        GRID_SIZE (int): Grid dimensions
        
    Returns:
        int: Number of lines cleared (rows + columns)
    """
    lines_cleared = 0
    
    # Identify completed rows and columns
    rows_to_clear = [
        y for y in range(GRID_SIZE)
        if all(cell != BLACK for cell in grid[y])
    ]
    
    cols_to_clear = [
        x for x in range(GRID_SIZE)
        if all(grid[y][x] != BLACK for y in range(GRID_SIZE))
    ]
    
    # Clear rows
    for y in rows_to_clear:
        grid[y] = [BLACK] * GRID_SIZE
        lines_cleared += 1
        
    # Clear columns
    for x in cols_to_clear:
        for y in range(GRID_SIZE):
            grid[y][x] = BLACK
        lines_cleared += 1
        
    return lines_cleared

def snap_to_grid(x, y, block, grid, GRID_SIZE, snap_range=20):
    """
    Snaps block coordinates to nearest valid grid position within snap range.
    
    Args:
        x,y (int): Pixel coordinates of block
        block (list[list]): Block being placed
        grid (list[list]): Current game state
        GRID_SIZE (int): Grid dimensions
        snap_range (int): Max pixel distance for snapping
        
    Returns:
        tuple(int,int) or None: Grid coordinates if valid snap exists
    """
    # Convert to grid coordinates
    grid_x = round(x / BLOCK_SIZE)
    grid_y = round(y / BLOCK_SIZE)
    
    # Check if within snap range and valid placement
    if (abs(x - grid_x * BLOCK_SIZE) <= snap_range and
        abs(y - grid_y * BLOCK_SIZE) <= snap_range and
        can_place_block(block, grid_x, grid_y, grid, GRID_SIZE)):
        return grid_x, grid_y
    return None

def are_blocks_equal(b1, b2):
    """
    Compares two blocks for exact equality in shape and filled cells.
    
    Args:
        b1, b2 (list[list]): Blocks to compare
        
    Returns:
        bool: True if blocks are identical
    """
    return (len(b1) == len(b2) and 
            all(len(r1) == len(r2) for r1, r2 in zip(b1, b2)) and 
            all(c1 == c2 for r1, r2 in zip(b1, b2) for c1, c2 in zip(r1, r2)))