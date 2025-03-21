from cst import *
import random

# Helper functions
def get_rotations(block):
    rotations = [block]
    for _ in range(3):
        block = [list(row) for row in zip(*block[::-1])]
        rotations.append(block)
    return rotations

def can_place_block(block, x, y, grid, GRID_SIZE, tolerance=2):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:  # Se a célula do bloco estiver ocupada
                # Calcula a posição no grid
                grid_x = x + col
                grid_y = y + row

                # Verifica se a posição está dentro dos limites do grid
                if (grid_x < 0 or grid_x >= GRID_SIZE or
                    grid_y < 0 or grid_y >= GRID_SIZE):
                    return False

                # Verifica se a célula do grid já está ocupada
                if grid[grid_y][grid_x] != BLACK:
                    return False  # Não pode sobrepor outra peça
    return True  # Todas as células estão livres

def place_block(block, x, y, color, grid, GRID_SIZE):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                grid[y + row][x + col] = color
                print(f"Placed block at ({x + col}, {y + row})")


def no_valid_moves_left(grid, blocks, GRID_SIZE):
    for block, color in blocks:
        for rotation in get_rotations(block):
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid, GRID_SIZE):
                        return False  # At least one valid move exists
    return True  # No valid moves left

# game.py
def clear_completed_lines(grid, GRID_SIZE):
    lines_cleared = 0

    # Check for completed rows
    rows_to_clear = []
    for y in range(GRID_SIZE):  # Use GRID_SIZE
        if all(cell != BLACK for cell in grid[y]):
            rows_to_clear.append(y)

    # Check for completed columns
    cols_to_clear = []
    for x in range(GRID_SIZE):  # Use GRID_SIZE
        if all(grid[y][x] != BLACK for y in range(GRID_SIZE)):  # Use GRID_SIZE
            cols_to_clear.append(x)

    # Clear completed rows
    for y in rows_to_clear:
        for x in range(GRID_SIZE):  # Use GRID_SIZE
            grid[y][x] = BLACK
        lines_cleared += 1

    # Clear completed columns
    for x in cols_to_clear:
        for y in range(GRID_SIZE):  # Use GRID_SIZE
            grid[y][x] = BLACK
        lines_cleared += 1

    return lines_cleared

def place_random_block(grid, blocks):
    if not blocks:
        print("No blocks left to place!")
        return grid, blocks
    remaining_blocks = blocks.copy()
    while remaining_blocks:
        block, color = random.choice(remaining_blocks)
        rotations = get_rotations(block)
        for rotation in rotations:
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid):
                        place_block(rotation, x, y, color, grid)
                        blocks.remove((block, color))
                        return grid, blocks
        remaining_blocks.remove((block, color))
    print("No valid placement found for any block!")
    return grid, blocks

def snap_to_grid(x, y, block, grid, GRID_SIZE, snap_range=20):
    # Calculate the nearest cell
    cell_x = round(x / BLOCK_SIZE) * BLOCK_SIZE
    cell_y = round(y / BLOCK_SIZE) * BLOCK_SIZE

    grid_x = cell_x // BLOCK_SIZE
    grid_y = cell_y // BLOCK_SIZE

    # Check if the adjusted position is valid (does not cause overlap)
    if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE):
        return grid_x, grid_y  # Return the adjusted and valid position
    else:
        return None  # Return None if the position is not valid
    