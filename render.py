"""
Game rendering module for Wood Block Puzzle.

Handles all visual aspects including:
- Game board rendering
- Block drawing and dragging
- Score display
- UI layout calculations
"""

import pygame
if not pygame.font.get_init():
    pygame.font.init()
from cst import *

def calculate_board_position(GRID_SIZE):
    """
    Calculates the board position and dimensions based on grid size.
    
    Args:
        GRID_SIZE (int): Current grid dimension (N x N)
        
    Returns:
        dict: Contains board position and dimensions with keys:
            - 'x': Left position (centered horizontally)
            - 'y': Top position (fixed margin)
            - 'width': Total board width in pixels
            - 'height': Total board height in pixels
    """
    board_width = GRID_SIZE * BLOCK_SIZE
    board_height = GRID_SIZE * BLOCK_SIZE
    return {
        'x': (WIDTH - board_width) // 2,  # Center horizontally
        'y': 50,                          # Fixed top margin
        'width': board_width,
        'height': board_height
    }

def draw_grid(screen, grid, GRID_SIZE, board_pos):
    """
    Renders the game grid with colored blocks and grid lines.
    
    Args:
        screen (pygame.Surface): Display surface to draw on
        grid (list[list[tuple]]): 2D array of RGB colors
        GRID_SIZE (int): Current grid dimension
        board_pos (dict): Board position and dimensions
        
    Note:
        Draws each cell with its color and a dark gray border
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(
                board_pos['x'] + x * BLOCK_SIZE,
                board_pos['y'] + y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE
            )
            pygame.draw.rect(screen, grid[y][x], rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Grid lines

def draw_blocks(screen, blocks, selected_index=None):
    """
    Renders available blocks in the bottom panel.
    
    Args:
        screen (pygame.Surface): Display surface
        blocks (list): Available (block_matrix, color) tuples
        selected_index (int, optional): Index of currently selected block
        
    Features:
        - Gray background panel
        - Centered block arrangement
        - Highlight for selected block
        - Proportional spacing between blocks
    """
    PANEL_HEIGHT = 120
    PANEL_Y = HEIGHT - PANEL_HEIGHT
    
    
    # Calculate centered positioning
    total_width = len(blocks) * 120  # 120px spacing per block
    start_x = (WIDTH - total_width) // 2
    
    for i, (block, color) in enumerate(blocks):
        block_x = start_x + i * 120
        block_y = PANEL_Y + 20  # 20px from panel top
        
        # Highlight selected block
        if i == selected_index:
            pygame.draw.rect(screen, (150, 150, 150), 
                           (block_x - 5, block_y - 5, 
                            BLOCK_SIZE * 3 + 10, BLOCK_SIZE * 3 + 10), 3)
        
        # Draw block cells
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    pygame.draw.rect(screen, color,
                                   (block_x + col * BLOCK_SIZE,
                                    block_y + row * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))

def render_score(screen, score, board_pos):
    """
    Displays the current score below the game board.
    
    Args:
        screen (pygame.Surface): Display surface
        score (int): Current player score
        board_pos (dict): Board position for placement reference
        
    Style Features:
        - Custom font with bold style
        - Text shadow effect
        - Centered below game board
        - Themed brown colors
    """
    font_score = pygame.font.SysFont("Luckiest Guy", 35, bold=True)
    TEXT_COLOR = (50, 30, 10)      # Dark brown
    SHADOW_COLOR = (100, 70, 30)   # Light brown
    
    score_text = f"Score: {score}"
    text_surface = font_score.render(score_text, True, TEXT_COLOR)
    
    # Center below board
    score_x = board_pos['x'] + (board_pos['width'] - text_surface.get_width()) // 2
    score_y = board_pos['y'] + board_pos['height'] + 20  # 20px gap
    
    # Shadow effect
    screen.blit(font_score.render(score_text, True, SHADOW_COLOR), 
               (score_x + 2, score_y + 2))
    screen.blit(text_surface, (score_x, score_y))


wood_texture = pygame.image.load("assets/back.png") #Carrega a imagem de fundo que está nos assets
wood_texture = pygame.transform.scale(wood_texture, (WIDTH, HEIGHT))


def render(screen, grid, blocks, score, GRID_SIZE, dragging_block=None, mouse_pos=None):
    """
    Main rendering function that composes all game elements.
    
    Args:
        screen (pygame.Surface): Display surface
        grid (list[list[tuple]]): Game board state
        blocks (list): Available blocks
        score (int): Current score
        GRID_SIZE (int): Grid dimension
        dragging_block (tuple, optional): (block, color, index) of dragged block
        mouse_pos (tuple, optional): Current (x,y) mouse position
        
    Returns:
        dict: Calculated board position for input handling
        
    Rendering Order:
        1. Background
        2. Game grid
        3. Block panel
        4. Dragged block (if any)
        5. Score display
    """
    board_pos = calculate_board_position(GRID_SIZE)
    
    # Clear screen
    screen.blit(wood_texture, (0,0))
    
    # Draw game elements
    draw_grid(screen, grid, GRID_SIZE, board_pos)
    draw_blocks(screen, blocks, dragging_block[0] if dragging_block else None)
    
    # Draw dragged block with transparency
    if dragging_block and mouse_pos:
        block, color, _ = dragging_block
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    s.fill((*color, 180))  # Semi-transparent
                    screen.blit(s, (mouse_pos[0] + col * BLOCK_SIZE, 
                                  mouse_pos[1] + row * BLOCK_SIZE))
    
    render_score(screen, score, board_pos)
    
    return board_pos