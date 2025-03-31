#cst.py
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]  # red, green, blue, yellow, purple
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
WOOD_BROWN = (139, 69, 19)

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
}
