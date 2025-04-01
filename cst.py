# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]  # red, green, blue, yellow, purple

BLOCK_PANEL_WIDTH = 150  # Width of the block selection panel
BLOCK_START_Y = 50      # Y-position where blocks start appearing
BLOCK_SPACING = 100     # Vertical space between blocks

BOARD_X = 50  # Example value - your actual board position
BOARD_Y = 50
BOARD_WIDTH = 600
BOARD_HEIGHT = 600

# Sizes
WIDTH = 800  #screen width
HEIGHT = 600  #screen height

# Grid settings
GRID_SIZE = 4  # Default grid size for Level 1
BLOCK_SIZE = 40  #


# Level-specific blocks
LEVEL_BLOCKS = {
    1: [
        ([[1, 1, 1]], (255, 0, 0)),  # (1,3) horizontal line, red
        ([[1], [1], [1]], (0, 255, 0)),  # (3,1) vertical line, green
        ([[1, 1], [0, 1]], (0, 0, 255)),  # Triangle corner, blue
        ([[1, 1], [1, 1]], (255, 255, 0))  # (2,2) square, yellow
    ],
    2: [
        ([[1, 1, 1, 1]], (255, 0, 0)),  # (1,4) horizontal line, red
        ([[1], [1], [1], [1]], (0, 255, 0)),  # (4,1) vertical line, green
        ([[1, 1], [0, 1]], (0, 0, 255)),  # Triangle corner, blue
        ([[1, 1], [1, 1]], (255, 255, 0))  # (2,2) square, yellow
    ],
    3: [
        ([[1, 1, 1]], (255, 0, 0)),  # (1,3) horizontal line, red
        ([[1], [1], [1], [1], [1]], (0, 255, 0)),  # (5,1) vertical line, green
        ([[1, 1], [1, 1], [1, 1]], (0, 0, 255)),  # (2,3) rectangle, blue
        ([[1, 1, 0], [0, 1, 1]], (255, 255, 0))  # (1,1,1,1) Z-shape, yellow
    ],
    4: [([[1,1]], (0, 255, 0))], # small rectangle
}
