import pygame 
from cst import *  

"""
    Draws the game grid on the screen.
    
    Args:
        screen (pygame.Surface): The Pygame surface where the grid will be drawn.
        grid (list): A 2D list representing the current state of the grid.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    """
def draw_grid(screen, grid, GRID_SIZE):
    for y in range(GRID_SIZE):  # Iterate over each row in the grid
        for x in range(GRID_SIZE):  # Iterate over each column in the grid
            # Draw a rectangle for each cell in the grid
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

"""
    Draws the available blocks on the side of the screen.
    
    Args:
        screen (pygame.Surface): The Pygame surface where the blocks will be drawn.
        blocks (list): A list of tuples representing the blocks and their colors.
    """
def draw_blocks(screen, blocks):
    for i, (block, color) in enumerate(blocks):  # Iterate over each block and its color
        for row in range(len(block)):  # Iterate over each row in the block
            for col in range(len(block[row])):  # Iterate over each column in the block
                if block[row][col]:  # If the cell in the block is filled (1)
                    # Draw the block at the appropriate position on the screen
                    pygame.draw.rect(screen, color, (WIDTH - 150 + col * BLOCK_SIZE, 50 + row * BLOCK_SIZE + i * 100, BLOCK_SIZE, BLOCK_SIZE))

"""
    Renders the entire game screen, including the grid, blocks, and score.
    
    Args:
        screen (pygame.Surface): The Pygame surface where everything will be drawn.
        grid (list): A 2D list representing the current state of the grid.
        blocks (list): A list of tuples representing the blocks and their colors.
        score (int): The player's current score.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    """
def render(screen, grid, blocks, score, GRID_SIZE):
    screen.fill(WHITE)  # Fill the screen with a white background
    
    draw_grid(screen, grid, GRID_SIZE)  # Draw the game grid
    
    draw_blocks(screen, blocks)  # Draw the available blocks
    
    # Render the score text
    font = pygame.font.SysFont("Arial", 24)  # Create a font object
    text = font.render(f"Score: {score}", True, WHITE)  # Create a text surface
    screen.blit(text, (10, 10))  # Draw the text on the screen at position (10, 10)
    
    pygame.display.flip()  # Update the display to show the rendered content