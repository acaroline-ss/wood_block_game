"""
cst.py - Constants module for a block puzzle game.

This module contains all the game constants including colors, dimensions,
assets paths, and level configurations. It's designed to be imported
by other game modules to maintain consistent configuration across the game.
"""

import pygame
import os

# Initialize pygame (required for font handling)
pygame.init()

# Color Constants
WHITE = (255, 255, 255)        # RGB value for white
BLACK = (0, 0, 0)              # RGB value for black
COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255)   # Purple
]

# UI Layout Constants
BLOCK_PANEL_WIDTH = 120        # Width of the block selection panel (pixels)
BLOCK_START_Y = 50             # Y-coordinate where blocks start appearing
BLOCK_SPACING = 120            # Vertical spacing between blocks
BOARD_X = 50                   # Board's left position
BOARD_Y = 50                   # Board's top position
BOARD_WIDTH = 600              # Board width
BOARD_HEIGHT = 600             # Board height
WIDTH = 700                    # Screen width
HEIGHT = 750                   # Screen height
GRID_SIZE = 4                  # Default grid size for Level 1
BLOCK_SIZE = 40                # Size of individual blocks (pixels)

# Menu Assets Dictionary
MENU_ASSETS = {
    "main_bg": "assets/sem_menu.png",
    "modes_bg": "assets/sem_menu.png", 
    "levels_bg": "assets/sem_menu.png",
    "algorithm_bg" : "assets/sem_menu.png",
    "tabua1": "assets/tabua1.png",
}

# PC Mode Color Scheme
PC_MODE_COLORS = {
    "title": (255, 180, 0),    # Gold color for titles
    "subtitle": (240, 240, 240) # Ice white for subtitles
}

# Level Configurations
# Dictionary mapping level numbers to their available block shapes and colors
# Each block is defined by a 2D matrix (shape) and an RGB color tuple
LEVEL_BLOCKS = {
    1: [
        ([[1, 1, 1]], (255, 0, 0)),          # 1x3 horizontal line (red)
        ([[1], [1], [1]], (0, 255, 0)),      # 3x1 vertical line (green)
        ([[1, 1], [0, 1]], (0, 0, 255)),     # L-shape (blue)
        ([[1, 1], [1, 1]], (255, 255, 0))    # 2x2 square (yellow)
    ],
    2: [
        ([[1, 1, 1, 1]], (255, 0, 0)),      # 1x4 horizontal line (red)
        ([[1], [1], [1], [1]], (0, 255, 0)), # 4x1 vertical line (green)
        ([[1, 1], [0, 1]], (0, 0, 255)),     # L-shape (blue)
        ([[1, 1], [1, 1]], (255, 255, 0))    # 2x2 square (yellow)
    ],
    3: [
        ([[1, 1, 1]], (255, 0, 0)),          # 1x3 horizontal line (red)
        ([[1], [1], [1], [1], [1]], (0, 255, 0)),  # 5x1 vertical line (green)
        ([[1, 1], [1, 1], [1, 1]], (0, 0, 255)),   # 2x3 rectangle (blue)
        ([[1, 1, 0], [0, 1, 1]], (255, 255, 0))   # Z-shape (yellow)
    ],
    4: [
        ([[1, 1]], (0, 255, 0))              # Small rectangle (green)
    ]
}

# Font Initialization with Fallback System
try:
    if os.path.exists("fonts/LuckiestGuy-Regular.ttf"):
        TITLE_FONT = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 64)
        SUBTITLE_FONT = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 20)
    else:
        raise FileNotFoundError("Font file not found at specified path")
except Exception as e:
    print(f"Error loading font: {e} - Using fallback system fonts")
    try:
        TITLE_FONT = pygame.font.SysFont("Impact", 64)
        SUBTITLE_FONT = pygame.font.SysFont("Impact", 30)
    except:
        TITLE_FONT = pygame.font.SysFont(None, 64)
        SUBTITLE_FONT = pygame.font.SysFont(None, 30)