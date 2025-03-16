# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

#sizes
WIDTH = 800
HEIGHT = 600

# Block shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1], [1, 1]],         # Square
    [[1, 1, 1, 1]],            # Line
    [[1, 1, 0], [0, 1, 1]],    # Z-shape
    [[0, 1, 1], [1, 1, 0]],    # S-shape
    [[1, 0], [1, 0], [1, 1]],  # L-shape
    [[0, 1], [0, 1], [1, 1]],  # Reverse L-shape
]

# Grid settings
GRID_SIZE = 5  # Default size (can be changed)
BLOCK_SIZE = 40