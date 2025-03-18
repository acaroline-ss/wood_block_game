# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]  # red, green, blue, yellow, purple

# Sizes
WIDTH = 800  # TODO: WHAT IS THIS FOR
HEIGHT = 600  # TODO

# Grid settings
GRID_SIZE = 4  # Default grid size for Level 1
BLOCK_SIZE = 40  # TODO: Adjust as needed

# Level-specific blocks
LEVEL_BLOCKS = {
    1: [
        [[1, 1, 1]],  # (1,3) horizontal line
        [[1], [1], [1]],  # (3,1) vertical line
        [[1, 1], [0, 1]],  # Triangle corner
        [[1, 1], [1, 1]],  # (2,2) square
    ],
    2: [
        [[1, 1, 1, 1]],  # (1,4) horizontal line
        [[1], [1], [1], [1]],  # (4,1) vertical line
        [[1, 1], [0, 1]],  # Triangle corner
        [[1, 1], [1, 1]],  # (2,2) square
    ],
    3: [
        [[1, 1, 1]],  # (1,3) horizontal line
        [[1], [1], [1], [1], [1]],  # (5,1) vertical line
        [[1, 1], [1, 1], [1, 1]],  # (2,3) rectangle
        [[1, 1, 0], [0, 1, 1]],  # (1,1,1,1) Z-shape
    ],
}
