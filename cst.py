"""
Wood Block Puzzle Game - Constants and Configuration

This module contains color definitions, game dimensions, and level configurations
for a wood block puzzle game. The game involves placing tetris-like blocks on a grid.
"""

# Color definitions in RGB format
WHITE = (255, 255, 255)  # Used for backgrounds or text
BLACK = (0, 0, 0)        # Used for text or outlines

# Block colors - each block type has a distinct color for visual differentiation
COLORS = [
    (255, 0, 0),     # red - typically for line blocks
    (0, 255, 0),     # green - typically for vertical blocks
    (0, 0, 255),     # blue - typically for L-shaped blocks
    (255, 255, 0),   # yellow - typically for square blocks
    (255, 0, 255)    # purple - typically for special shapes
]

# Game board dimensions and layout
BOARD_X = 50         # X position of the game board (pixels from left)
BOARD_Y = 50         # Y position of the game board (pixels from top)
BOARD_WIDTH = 600    # Total width of the game board
BOARD_HEIGHT = 600   # Total height of the game board

# Screen dimensions
WIDTH = 800          # Total window width (includes board + block panel)
HEIGHT = 600         # Total window height

# Block selection panel dimensions
BLOCK_PANEL_WIDTH = 150   # Width of the side panel for block selection
BLOCK_START_Y = 50        # Starting Y position for block display in panel
BLOCK_SPACING = 100       # Vertical spacing between blocks in panel

# Grid and block settings
GRID_SIZE = 4        # Default grid size (4x4) for initial levels
BLOCK_SIZE = 40      # Size of each grid cell in pixels

# Level configurations
# Each level defines the available blocks and their properties
# Format: level_number: [ (block_matrix, block_color), ... ]
# Where block_matrix is a 2D list representing the block shape (1=occupied, 0=empty)
LEVEL_BLOCKS = {
    1: [
        # Horizontal 3-block line
        ([[1, 1, 1]], (255, 0, 0)),
        # Vertical 3-block line
        ([[1], [1], [1]], (0, 255, 0)),
        # L-shaped block (2x2 with one empty cell)
        ([[1, 1], [0, 1]], (0, 0, 255)),
        # 2x2 square block
        ([[1, 1], [1, 1]], (255, 255, 0))
    ],
    2: [
        # Horizontal 4-block line (longer than level 1)
        ([[1, 1, 1, 1]], (255, 0, 0)),
        # Vertical 4-block line
        ([[1], [1], [1], [1]], (0, 255, 0)),
        # L-shaped block (same as level 1)
        ([[1, 1], [0, 1]], (0, 0, 255)),
        # 2x2 square block (same as level 1)
        ([[1, 1], [1, 1]], (255, 255, 0))
    ],
    3: [
        # Horizontal 3-block line (shorter than level 2)
        ([[1, 1, 1]], (255, 0, 0)),
        # Vertical 5-block line (longer than previous levels)
        ([[1], [1], [1], [1], [1]], (0, 255, 0)),
        # 2x3 rectangle block
        ([[1, 1], [1, 1], [1, 1]], (0, 0, 255)),
        # Z-shaped tetromino
        ([[1, 1, 0], [0, 1, 1]], (255, 255, 0))
    ],
}