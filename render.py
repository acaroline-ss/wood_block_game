import pygame 
from cst import *  

"""
    Draws the game grid on the screen.
    
    Args:
        screen (pygame.Surface): The Pygame surface where the grid will be drawn.
        grid (list): A 2D list representing the current state of the grid.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    """
# Configurações do tabuleiro
BOARD_X = 50          # Posição X do canto superior esquerdo do tabuleiro
BOARD_Y = 50          # Posição Y do canto superior esquerdo do tabuleiro
BOARD_WIDTH = 100     # Largura do tabuleiro
BOARD_HEIGHT = 110    # Altura do tabuleiro

def draw_grid(screen, grid, GRID_SIZE):
    for y in range(GRID_SIZE):  # Iterate over each row in the grid
        for x in range(GRID_SIZE):  # Iterate over each column in the grid
            # Draw a rectangle for each cell in the grid
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

"""
    Draws the available blocks on the side of the screen.
    
    Args:
        screen (pygame.Surface): The Pygame surface where the blocks will be drawn.
        blocks (list): A list of tuples representing the blocks and their colors.
    """
def draw_blocks(screen, blocks, selected_index=None):
    for i, (block, color) in enumerate(blocks):
        if i != selected_index:  # Não renderiza o bloco selecionado (está sendo arrastado)
            pygame.draw.rect(screen, (200, 200, 200), (WIDTH - 150, 50 + i * 100, 3 * BLOCK_SIZE, 3 * BLOCK_SIZE))
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (WIDTH - 150 + col * BLOCK_SIZE, 50 + i * 100 + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

"""
    Renders the entire game screen, including the grid, blocks, and score.
    
    Args:
        screen (pygame.Surface): The Pygame surface where everything will be drawn.
        grid (list): A 2D list representing the current state of the grid.
        blocks (list): A list of tuples representing the blocks and their colors.
        score (int): The player's current score.
        GRID_SIZE (int): The size of the grid (number of rows and columns).
    """
def render(screen, grid, blocks, score, GRID_SIZE, dragging_block=None, mouse_pos=None):
    # 1. Limpe a tela UMA vez
    screen.fill(WHITE)
    
    # 2. Desenhe elementos estáticos
    draw_grid(screen, grid, GRID_SIZE)
    
    # 3. Desenhe blocos laterais (exceto o arrastado)
    selected_idx = dragging_block[0] if dragging_block else None
    draw_blocks(screen, blocks, selected_idx)
    
    # 4. Desenhe o bloco arrastado (COM TRANSPARÊNCIA)
    if dragging_block and mouse_pos:
        block, color, _ = dragging_block
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    # Crie superfície transparente
                    s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    s.fill((color[0], color[1], color[2], 180))  # Alpha=180 (semi-transparente)
                    screen.blit(s, (mouse_pos[0] + col * BLOCK_SIZE, mouse_pos[1] + row * BLOCK_SIZE))
    
    # 5. UI (score)
    # Configurações do score
    font_score = pygame.font.SysFont("Luckiest Guy", 35, bold=True)

    # Posição X: Alinhado à direita do tabuleiro (BOARD_X + BOARD_WIDTH - largura_do_texto)
    # Posição Y: 5px abaixo do tabuleiro (como você já estava usando)
    score_y = BOARD_Y + BOARD_HEIGHT + 5

    # Renderiza o texto uma vez para calcular sua largura
    text = font_score.render(f"Score: {score}", True, (0, 0, 0))  # Cor temporária
    text_width = text.get_width()

    # Calcula a posição X para alinhar à direita do tabuleiro
    score_x = BOARD_X + BOARD_WIDTH - text_width  # Alinhado à direita

    # Cores (marrom escuro e sombra)
    TEXT_COLOR = (50, 30, 10)    # Cor principal (marrom madeira)
    SHADOW_COLOR = (100, 70, 30)  # Sombra sutil

    # Renderiza o score
    shadow_text = font_score.render(f"Score: {score}", True, SHADOW_COLOR)
    screen.blit(shadow_text, (score_x + 2, score_y + 2))  # Sombra

    main_text = font_score.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(main_text, (score_x, score_y))  # Texto principal
