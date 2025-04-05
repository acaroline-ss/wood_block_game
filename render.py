import pygame
from cst import *

# Board display constants
BOARD_X = 50          # X position of board's top-left corner
BOARD_Y = 50          # Y position of board's top-left corner
BOARD_WIDTH = 100     # Total width of the game board
BOARD_HEIGHT = 110    # Total height of the game board
TEXT_COLOR = (50, 30, 10)    # Primary text color (wood brown)
SHADOW_COLOR = (100, 70, 30)  # Text shadow color

def draw_grid(screen, grid, grid_size):
    """
    Draws the game grid with cell borders.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        grid (list[list]): 2D array representing cell colors
        grid_size (int): Number of rows/columns in the grid
    """
    for y in range(grid_size):
        for x in range(grid_size):
            # Draw cell fill
            pygame.draw.rect(
                screen, 
                grid[y][x], 
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            )
            # Draw cell border
            pygame.draw.rect(
                screen, 
                (50, 50, 50), 
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 
                1
            )

def draw_blocks(screen, blocks, selected_index=None):
    """
    Draws available blocks in the sidebar, excluding the selected one.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        blocks (list): List of (block_matrix, color) tuples
        selected_index (int, optional): Index of block being dragged
    """
    for i, (block, color) in enumerate(blocks):
        if i != selected_index:  # Skip the dragged block
            # Draw block container background
            pygame.draw.rect(
                screen, 
                (200, 200, 200), 
                (WIDTH - 150, 50 + i * 100, 3 * BLOCK_SIZE, 3 * BLOCK_SIZE)
            )
            
            # Draw each cell of the block
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(
                            screen,
                            color,
                            (WIDTH - 150 + col * BLOCK_SIZE, 
                             50 + i * 100 + row * BLOCK_SIZE, 
                             BLOCK_SIZE, BLOCK_SIZE)
                        )

def draw_dragging_block(screen, dragging_block, mouse_pos):
    """
    Draws a semi-transparent version of the block being dragged.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        dragging_block (tuple): (block_matrix, color, original_index)
        mouse_pos (tuple): Current (x,y) mouse position
    """
    block, color, _ = dragging_block
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                # Create transparent surface
                s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                s.fill((*color, 180))  # Semi-transparent
                screen.blit(
                    s, 
                    (mouse_pos[0] + col * BLOCK_SIZE, 
                     mouse_pos[1] + row * BLOCK_SIZE)
                )

def draw_score(screen, score):
    """
    Renders the score display with shadow effect.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        score (int): Current player score
    """
    font = pygame.font.SysFont("Luckiest Guy", 35, bold=True)
    score_text = f"Score: {score}"
    
    # Calculate position to right-align with board
    text = font.render(score_text, True, (0, 0, 0))
    score_x = BOARD_X + BOARD_WIDTH - text.get_width()
    score_y = BOARD_Y + BOARD_HEIGHT + 5
    
    # Draw shadow and main text
    shadow = font.render(score_text, True, SHADOW_COLOR)
    screen.blit(shadow, (score_x + 2, score_y + 2))
    main_text = font.render(score_text, True, TEXT_COLOR)
    screen.blit(main_text, (score_x, score_y))

def render(screen, grid, blocks, score, grid_size, dragging_block=None, mouse_pos=None):
    """
    Main rendering function that composes all game elements.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        grid (list[list]): 2D array representing the game state
        blocks (list): Available blocks (block_matrix, color)
        score (int): Current player score
        grid_size (int): Size of the game grid
        dragging_block (tuple, optional): Block being dragged
        mouse_pos (tuple, optional): Current mouse position
    """
    screen.fill(WHITE)
    draw_grid(screen, grid, grid_size)
    
    selected_idx = dragging_block[2] if dragging_block else None
    draw_blocks(screen, blocks, selected_idx)
    
    if dragging_block and mouse_pos:
        draw_dragging_block(screen, dragging_block, mouse_pos)
    
    draw_score(screen, score)

def render_game_only(screen, grid, blocks, grid_size, dragging_block=None, mouse_pos=None):
    """
    Lightweight renderer without score display (for AI/preview uses).
    
    Args:
        screen (pygame.Surface): Surface to draw on
        grid (list[list]): 2D array representing the game state
        blocks (list): Available blocks (block_matrix, color)
        grid_size (int): Size of the game grid
        dragging_block (tuple, optional): Block being dragged
        mouse_pos (tuple, optional): Current mouse position
    """
    screen.fill(WHITE)
    draw_grid(screen, grid, grid_size)
    
    selected_idx = dragging_block[2] if dragging_block else None
    draw_blocks(screen, blocks, selected_idx)
    
    if dragging_block and mouse_pos:
        draw_dragging_block(screen, dragging_block, mouse_pos)