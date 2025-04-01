from cst import * 
import random 

# Helper functions
"""
    Generates all possible rotations of a block.
    
    Args:
        block (list): A 2D list representing the block.
    
    Returns:
        list: A list of all possible rotations of the block.
    """
def get_rotations(block):
    rotations = [block]  # Start with the original block
    for _ in range(3):  # Rotate the block 3 more times (90°, 180°, 270°)
        block = [list(row) for row in zip(*block[::-1])]  # Rotate the block 90 degrees
        rotations.append(block)  # Add the rotated block to the list
    return rotations  # Return all rotations

"""
    Checks if a block can be placed at a specific position on the grid.
    
    Args:
        block (list): A 2D list representing the block.
        x (int): The x-coordinate on the grid.
        y (int): The y-coordinate on the grid.
        grid (list): A 2D list representing the current state of the grid.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
        tolerance (int): Optional parameter for tolerance (not used in this function).
    
    Returns:
        bool: True if the block can be placed, False otherwise.
    """
def can_place_block(block, x, y, grid, GRID_SIZE, tolerance=None):
    for row in range(len(block)):  # Iterate over each row in the block
        for col in range(len(block[row])):  # Iterate over each column in the block
            if block[row][col]:  # If the cell in the block is filled (1)
                grid_x = x + col  # Calculate the x-coordinate on the grid
                grid_y = y + row  # Calculate the y-coordinate on the grid

                # Check if the block is within the grid boundaries
                if grid_x < 0 or grid_x >= GRID_SIZE or grid_y < 0 or grid_y >= GRID_SIZE:
                    return False  # Block is out of bounds

                # Check if the cell on the grid is already occupied
                if grid[grid_y][grid_x] != BLACK:
                    return False  # Cell is occupied

    return True  # Block can be placed

"""
    Places a block on the grid at a specific position.
    
    Args:
        block (list): A 2D list representing the block.
        x (int): The x-coordinate on the grid.
        y (int): The y-coordinate on the grid.
        color (tuple): The color of the block (RGB tuple).
        grid (list): A 2D list representing the current state of the grid.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    """
def place_block(block, x, y, color, grid, GRID_SIZE):
    for row in range(len(block)):  # Iterate over each row in the block
        for col in range(len(block[row])):  # Iterate over each column in the block
            if block[row][col]:  # If the cell in the block is filled (1)
                grid[y + row][x + col] = color  # Place the block on the grid
                print(f"Placed block at ({x + col}, {y + row})")  # Print the placement position

"""
    Checks if there are no valid moves left for the remaining blocks.
    
    Args:
        grid (list): A 2D list representing the current state of the grid.
        blocks (list): A list of tuples representing the remaining blocks and their colors.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    
    Returns:
        bool: True if no valid moves are left, False otherwise.
    """
def no_valid_moves_left(grid, blocks, GRID_SIZE):
    for block, color in blocks:  # Iterate over each block and its color
        for rotation in get_rotations(block):  # Check all rotations of the block
            for x in range(GRID_SIZE):  # Iterate over each x-coordinate on the grid
                for y in range(GRID_SIZE):  # Iterate over each y-coordinate on the grid
                    if can_place_block(rotation, x, y, grid, GRID_SIZE):  # Check if the block can be placed
                        return False  # At least one valid move exists
    return True  # No valid moves left

"""
    Clears completed rows and columns on the grid and returns the number of lines cleared.
    
    Args:
        grid (list): A 2D list representing the current state of the grid.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    
    Returns:
        int: The number of lines cleared.
    """
def clear_completed_lines(grid, GRID_SIZE):
    print(f"Debug: GRID_SIZE = {GRID_SIZE}")  # Debug print
    print(f"Debug: Actual grid dimensions = {len(grid)}x{len(grid[0]) if grid else 0}")  # Debug print

    lines_cleared = 0  # Counter for cleared lines

    # Check for completed rows
    rows_to_clear = []  # List to store indices of completed rows
    for y in range(GRID_SIZE):  # Iterate over each row
        if all(cell != BLACK for cell in grid[y]):   # Check if all cells in the row are filled
            rows_to_clear.append(y)  # Add the row index to the list

    # Check for completed columns
    cols_to_clear = []  # List to store indices of completed columns
    for x in range(GRID_SIZE):  # Iterate over each column
        if all(grid[y][x] != BLACK for y in range(GRID_SIZE)): # Check if all cells in the column are filled
            cols_to_clear.append(x)  # Add the column index to the list

    # Clear completed rows
    for y in rows_to_clear:  # Iterate over each completed row
        for x in range(GRID_SIZE):  # Iterate over each cell in the row
            grid[y] = [BLACK for _ in range(GRID_SIZE)]  # Clear the cell
        lines_cleared += 1  # Increment the counter

    # Clear completed columns
    for x in cols_to_clear:  # Iterate over each completed column
        for y in range(GRID_SIZE):  # Iterate over each cell in the column
            grid[y][x] = BLACK  # Clear the cell
        lines_cleared += 1  # Increment the counter

    return lines_cleared  # Return the number of lines cleared

"""
    Snaps a block to the nearest valid position on the grid.
    
    Args:
        x (int): The x-coordinate of the block's position.
        y (int): The y-coordinate of the block's position.
        block (list): A 2D list representing the block.
        grid (list): A 2D list representing the current state of the grid.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
        snap_range (int): The range within which snapping is allowed (default is 20).
    
    Returns:
        tuple: The snapped (x, y) position if valid, otherwise None.
    """
def snap_to_grid(x, y, block, grid, GRID_SIZE, snap_range=20):
    # Calculate the nearest cell
    cell_x = round(x / BLOCK_SIZE) * BLOCK_SIZE  # Snap x-coordinate to the nearest grid cell
    cell_y = round(y / BLOCK_SIZE) * BLOCK_SIZE  # Snap y-coordinate to the nearest grid cell

    grid_x = cell_x // BLOCK_SIZE  # Convert to grid index
    grid_y = cell_y // BLOCK_SIZE  # Convert to grid index

    # Check if the snapped position is valid
    if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE):
        return grid_x, grid_y  # Return the snapped position
    else:
        return None  # Return None if the position is invalid