#cst.py
import pygame
import os
# Colors
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]  # red, green, blue, yellow, purple

BLOCK_PANEL_WIDTH = 120  # Width of the block selection panel
BLOCK_START_Y = 50      # Y-position where blocks start appearing
BLOCK_SPACING = 120   
# Configurações do painel inferi

BOARD_X = 50  # Example value - your actual board position
BOARD_Y = 50
BOARD_WIDTH = 600
BOARD_HEIGHT = 600

# Menu Assets
MENU_ASSETS = {
    "main_bg": "assets/sem_menu.png",
    "modes_bg": "assets/sem_menu.png", 
    "levels_bg": "assets/sem_menu.png",
    "tabua1": "assets/tabua1.png",
    "tabua1": "assets/tabua1.png",
    "tabua1": "assets/tabua1.png",
}

PC_MODE_COLORS = {
    "title": (255, 180, 0),    # Dourado
    "subtitle": (240, 240, 240) # Branco gelo
}


# Sizes
WIDTH = 700  #screen width
HEIGHT = 750  #screen height

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
try:
    # Verifica se o arquivo existe antes de carregar
    if os.path.exists("fonts/LuckiestGuy-Regular.ttf"):
        TITLE_FONT = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 64)
        SUBTITLE_FONT = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 48)
    else:
        raise FileNotFoundError("Fonte não encontrada no caminho especificado")
except Exception as e:
    print(f"Erro ao carregar fonte: {e} - Usando fallback")
    try:
        
        TITLE_FONT = pygame.font.SysFont("Impact", 64)
        SUBTITLE_FONT = pygame.font.SysFont("Impact", 28)
    except:
        TITLE_FONT = pygame.font.SysFont(None, 64)
        SUBTITLE_FONT = pygame.font.SysFont(None, 48)