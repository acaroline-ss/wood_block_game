import pygame
from cst import WHITE, BLACK, BLOCK_SIZE, GRID_SIZE, COLORS

def draw_grid(screen, grid):
    """
    Draw the grid on the screen.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_blocks(screen, blocks):
    """
    Draw the available blocks on the screen.
    """
    for i, (block, color) in enumerate(blocks):
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    pygame.draw.rect(screen, color, (screen.WIDTH - 150 + col * BLOCK_SIZE, 50 + row * BLOCK_SIZE + i * 100, BLOCK_SIZE, BLOCK_SIZE))

def render(screen, grid, blocks, score):
    """
    Render the entire game state (grid, blocks, and score).
    """
    screen.fill(WHITE)
    draw_grid(screen, grid)
    draw_blocks(screen, blocks)
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))
    pygame.display.flip()