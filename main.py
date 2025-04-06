"""
Wood Block Puzzle Game

A puzzle game where players place colored blocks on a grid to complete lines.
Features multiple game modes (human, computer, assisted) and search algorithms.
"""

import pygame
import random  
import time 
from render import * 
from cst import * 
from game import *  
from heuristics import *  
from search import * 
from visuals.victory import *
from visuals.levels import *
from visuals.game_over import *
from visuals.menu import *
from visuals.helpers import *
from assets import *
from visuals.buttons import *
import os
import sys
from pathlib import Path

# Garante que o Python comece a procurar arquivos na pasta do projeto
PROJECT_ROOT = Path(__file__).parent
os.chdir(PROJECT_ROOT)  # Muda o diretório de trabalho
sys.path.append(str(PROJECT_ROOT))  # Adiciona ao PATH do Python

print(f"Diretório corrigido para: {PROJECT_ROOT}")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wood Block Puzzle")
clock = pygame.time.Clock()

# Game state variables
grid = None          # Current game grid (2D list of colors)
blocks = []          # Available blocks to place
selected_block = None  # Currently selected/dragged block
score = 100            # Player's current score
current_level = 1    # Current level (1-3)
game_mode = None     # Current game mode ('human', 'pc', 'assistant')

class GameState:
    """Enum-like class for tracking game states."""
    MAIN_MENU = 0
    GAME_MODE = 1
    LEVEL_SELECT = 2
    GAME = 3
    GAME_OVER = 4
    VICTORY = 5

def show_main_menu(screen):
    font = pygame.font.SysFont("Luckiest Guy", 48)
    buttons = [
        {"text": "Jogar", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "action": GameState.LEVEL_SELECTION},
        {"text": "Sair", "rect": pygame.Rect(WIDTH//2-100, 280, 200, 50), "action": "quit"}
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Desenhar fundo
        try:
            bg = pygame.image.load(MENU_ASSETS["main_bg"]).convert()
            screen.blit(bg, (0, 0))
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
            screen.fill((139, 69, 19))  # Fallback
        
        # Desenhar título
        title = font.render("Wood Block Puzzle", True, (240, 220, 180))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Desenhar botões
        for btn in buttons:
            color = (100, 70, 30) if btn["rect"].collidepoint(mouse_pos) else (70, 40, 10)
            pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
            pygame.draw.rect(screen, (50, 30, 10), btn["rect"], 2, border_radius=8)
            
            btn_text = font.render(btn["text"], True, (240, 220, 180))
            text_rect = btn_text.get_rect(center=btn["rect"].center)
            screen.blit(btn_text, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return btn["action"]
    
def show_algorithm_menu(screen):
    font = pygame.font.SysFont("Luckiest Guy", 36)
    buttons = [
        {"text": "BFS", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "action": "bfs"},
        {"text": "DFS", "rect": pygame.Rect(WIDTH//2-100, 270, 200, 50), "action": "dfs"},
        {"text": "Greedy", "rect": pygame.Rect(WIDTH//2-100, 340, 200, 50), "action": "greedy"},
        {"text": "A*", "rect": pygame.Rect(WIDTH//2-100, 410, 200, 50), "action": "a_star"},
        {"text": "Voltar", "rect": pygame.Rect(WIDTH//2-100, 480, 200, 50), "action": "back"}
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Desenhar fundo
        try:
            bg = pygame.image.load(MENU_ASSETS["main_bg"]).convert()
            screen.blit(bg, (0, 0))
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
            screen.fill((139, 69, 19))  # Fallback
        
        # Draw title
        title_font = pygame.font.SysFont("Luckiest Guy", 48)
        title = title_font.render("Selecione o Algoritmo", True, (240, 220, 180))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw buttons
        for btn in buttons:
            color = (100, 70, 30) if btn["rect"].collidepoint(mouse_pos) else (70, 40, 10)
            pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
            pygame.draw.rect(screen, (50, 30, 10), btn["rect"], 2, border_radius=8)
            
            btn_text = font.render(btn["text"], True, (240, 220, 180))
            text_rect = btn_text.get_rect(center=btn["rect"].center)
            screen.blit(btn_text, text_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return btn["action"]

# Define grid sizes for each level
LEVEL_GRID_SIZES = {
    1: 4,  # Level 1: 4x4 grid
    2: 5,  # Level 2: 5x5 grid
    3: 6,  # Level 3: 6x6 grid
}

# Pre-filled grids for each level (from second code)
LEVEL_PRE_FILLED = {
    1: [  # Level 1 grid with some pre-filled cells
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    2: [  # Level 2 grid with some pre-filled cells
        [1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0]
    ],
    3: [  # Level 3 grid with some pre-filled cells
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0]
    ],
}

def initialize_level(level):
    """
    Initialize game state for a specific level (using second code's visual approach).
    """
    global GRID_SIZE, grid, blocks, target_moves, moves_made
    
    GRID_SIZE = LEVEL_GRID_SIZES[level]  # Set the grid size for the level
    # Create the grid by replacing 1s with random colors and 0s with BLACK
    grid = [[BLACK if cell == 0 else random.choice(COLORS) for cell in row] 
            for row in LEVEL_PRE_FILLED[level]]
    
    blocks = LEVEL_BLOCKS[level].copy()  # Create a fresh copy of blocks
    
    # Set target moves based on level (from first code)
    target_moves = {1: 5, 2: 12, 3: 44}.get(level, 5)
    moves_made = 0
    score = 100

def human_mode(level, screen):
    """
    Human player game mode with second code's visual representation.
    """
    global selected_block, grid, blocks, score, GRID_SIZE, moves_made, target_moves
    
    initialize_level(level)
    running = True
    dragging = False
    selected_index = None
    clock = pygame.time.Clock()
    FPS = 60

    while running:
        # Game state checks (from first code)
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            return ("game_over", score)
        if all(cell == BLACK for row in grid for cell in row):
            return ("victory", score)
        if score <= 0:
            return ("game_over", score)

        # Get board position for rendering (from second code)
        board_pos = render(screen, grid, blocks, score, GRID_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Block selection (from second code with first code's logic)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                PANEL_HEIGHT = 120
                PANEL_Y = HEIGHT - PANEL_HEIGHT
                
                # Check if click is in the blocks panel
                if 0 <= x <= WIDTH and PANEL_Y <= y <= HEIGHT:
                    BLOCK_SPACING = 120
                    total_width = len(blocks) * BLOCK_SPACING
                    start_x = (WIDTH - total_width) // 2
                    selected_index = (x - start_x) // BLOCK_SPACING
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
            
            # Block placement (from second code with first code's logic)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                if selected_block:
                    x, y = pygame.mouse.get_pos()
                    rel_x = x - board_pos['x']
                    rel_y = y - board_pos['y']
                    snapped_pos = snap_to_grid(rel_x, rel_y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    
                    if snapped_pos:
                        grid_x, grid_y = snapped_pos
                        block, color = selected_block
                        
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            moves_made += 1
                            
                            # Calculate score based on target moves (from first code)
                            if moves_made > target_moves:
                                score -= 20  # Deduct 20 points for each move beyond target
                            
                            # Add bonus for line/column clears
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            if moves_made > target_moves and lines_cleared > 0:
                                score += lines_cleared * 10
                            
                            # Remove used block and check if need to repopulate
                            if selected_index is not None and selected_index < len(blocks):
                                blocks.pop(selected_index)
                                if not blocks:
                                    blocks = LEVEL_BLOCKS[level].copy()
                            
                            if all(cell == BLACK for row in grid for cell in row):
                                return ("victory", score)
                
                # Reset dragging state
                selected_block = None
                dragging = False
                selected_index = None
                
            # Block rotation (from first code)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                block, color = selected_block
                # Rotate 90 degrees clockwise
                selected_block = ([list(row) for row in zip(*block[::-1])], color)

        # Rendering (from second code)
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw dragged block (from second code)
        if dragging and selected_block:
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(
                            screen, 
                            color,
                            (x + col * BLOCK_SIZE, 
                             y + row * BLOCK_SIZE,
                             BLOCK_SIZE,
                             BLOCK_SIZE)
                        )
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return "quit"  # Fallback

def pc_mode(algorithm, level, screen, heuristic=None):
    """
    Computer-controlled game mode using specified algorithm with second code's visual representation.
    """
    global grid, blocks, score, GRID_SIZE
    
    # Initialize level (using second code's approach)
    initialize_level(level)
    initial_state = State([row.copy() for row in grid], blocks.copy(), GRID_SIZE)
    
    # Time the algorithm execution
    start_time = time.time()
    
    # Run selected algorithm (from first code)
    algorithm_map = {
        "bfs": lambda s: bfs(s, level),
        "dfs": lambda s: dfs(s, level),
        "greedy": lambda s: greedy(s, heuristic_filled_cells, level),
        "a_star": lambda s: a_star(s, combined_heuristic, level)
    }
    
    solution_state = algorithm_map.get(algorithm, lambda s: None)(initial_state)
    elapsed_time = time.time() - start_time
    
    if not solution_state:
        return "game_over"
    
    # Reconstruct solution path
    path = []
    current = solution_state
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    # Prepare move information for display (from second code)
    move_info = []
    for idx, state in enumerate(path[1:], 1):
        if state.action:
            block, color, x, y = state.action
            block_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(block_surface, color, (col*10, row*10, 10, 10))
            move_info.append({
                "text": f"Move {idx}: ({x},{y})",
                "block": block_surface
            })

    # Create menu button using the same Button class as VictoryScreen
    menu_button = Button("MENU", (150, HEIGHT - 70), "main_menu")
    
    # Visualization loop (from second code with first code's logic)
    current_move = 0
    while current_move < len(path):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_move < len(path) - 1:
                    current_move += 1
                elif event.key == pygame.K_ESCAPE:
                    current_move = len(path) - 1
            # Handle button click - returns immediately if clicked
            if menu_button.handle_event(event):
                return menu_button.action  # Returns "main_menu"
        
        # Update game state from current move
        state = path[current_move]
        grid = [row.copy() for row in state.grid]
        blocks = state.blocks.copy()
        score = state.moves * 10  # From first code
        
        # Render game (from second code)
        screen.fill((139, 69, 19))  # Wood background
        render(screen, grid, blocks, score, GRID_SIZE)

        # Draw menu button
        menu_button.draw(screen)
        
        # Draw the right-side panel (from second code)
        panel_width = 250
        panel_x = WIDTH - panel_width - 10
        info_panel = pygame.Rect(panel_x, 10, panel_width, HEIGHT - 20)
        
        # Panel background
        pygame.draw.rect(screen, (100, 70, 30), info_panel, border_radius=8)
        pygame.draw.rect(screen, (50, 30, 10), info_panel, 2, border_radius=8)
        
        # Draw algorithm info (from second code)
        y_offset = 20
        fonts = {
            "title": pygame.font.SysFont("Luckiest Guy", 28),
            "info": pygame.font.SysFont("Arial", 20, bold=True),
            "move": pygame.font.SysFont("Arial", 16, bold=True)
        }
        
        # Title and stats
        title = fonts["title"].render(f"{algorithm.upper()} Solution", True, (240, 220, 180))
        screen.blit(title, (panel_x + (panel_width - title.get_width())//2, y_offset))
        y_offset += 40
        
        stats = [
            f"Level: {level}",
            f"Time: {elapsed_time:.2f}s",
            f"Moves: {current_move}/{len(path)-1}",
            f"Score: {score}"
        ]
        
        for text in stats:
            text_surface = fonts["info"].render(text, True, (240, 220, 180))
            screen.blit(text_surface, (panel_x + 15, y_offset))
            y_offset += 30
        
        # Move history (last 4 moves)
        if current_move > 0:
            y_offset += 10
            move_title = fonts["info"].render("Move History:", True, (240, 220, 180))
            screen.blit(move_title, (panel_x + 15, y_offset))
            y_offset += 30
            
            start_idx = max(0, current_move - 4)
            for i in range(start_idx, current_move):
                move = move_info[i]
                text_surface = fonts["move"].render(move["text"], True, (240, 220, 180))
                screen.blit(text_surface, (panel_x + 15, y_offset))
                screen.blit(move["block"], (panel_x + panel_width - 60, y_offset))
                y_offset += 40
        
        # Controls
        y_offset += 20
        controls_title = fonts["info"].render("Controls:", True, (240, 220, 180))
        screen.blit(controls_title, (panel_x + 15, y_offset))
        y_offset += 30
        
        for key, desc in [("SPACE", "Next move"), ("ESC", "Skip to end")]:
            key_text = fonts["move"].render(key, True, (240, 220, 180))
            desc_text = fonts["move"].render(desc, True, (240, 220, 180))
            screen.blit(key_text, (panel_x + 30, y_offset))
            screen.blit(desc_text, (panel_x + 100, y_offset))
            y_offset += 30
        
        pygame.display.flip()
        clock.tick(60)
    
    return "victory"

def computer_assisted_human_mode(level, screen):
    """
    Human player mode with computer hints (from first code with second code's visuals).
    """
    global selected_block, grid, blocks, score, GRID_SIZE, moves_made, target_moves
    
    initialize_level(level)
    running = True
    dragging = False
    selected_index = None
    hint_block = None
    hint_alpha = 100  # Hint transparency

    # Hint button setup (from first code)
    hint_button = pygame.Rect(WIDTH - 150, HEIGHT - 70, 120, 50)
    button_font = pygame.font.SysFont("Arial", 24)

    while running:
        # Game state checks (from first code)
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            return ("game_over", score)
        if all(cell == BLACK for row in grid for cell in row):
            return ("victory", score)
        if score <= 0:
            return ("game_over", score)

        # Get board position for rendering (from second code)
        board_pos = render(screen, grid, blocks, score, GRID_SIZE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Hint button or block selection (from first code)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                
                if hint_button.collidepoint(x, y):
                    # Get hint using greedy algorithm
                    current_state = State([row.copy() for row in grid], blocks.copy(), GRID_SIZE)
                    solution_state = greedy(current_state, heuristic_filled_cells, level)
                    
                    if solution_state and solution_state.parent:
                        path = []
                        current = solution_state
                        while current.parent:
                            path.append(current)
                            current = current.parent
                        path.reverse()
                        
                        if path and path[0].action:
                            block, color, x, y = path[0].action
                            hint_block = (block, color, x, y)
                
                # Block selection (from second code)
                elif 0 <= x <= WIDTH and HEIGHT-120 <= y <= HEIGHT:
                    BLOCK_SPACING = 120
                    total_width = len(blocks) * BLOCK_SPACING
                    start_x = (WIDTH - total_width) // 2
                    selected_index = (x - start_x) // BLOCK_SPACING
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
                        hint_block = None  # Clear hint on new selection
                        
            # Block placement (from second code with first code's logic)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                if selected_block:
                    x, y = pygame.mouse.get_pos()
                    rel_x = x - board_pos['x']
                    rel_y = y - board_pos['y']
                    snapped_pos = snap_to_grid(rel_x, rel_y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    
                    if snapped_pos:
                        grid_x, grid_y = snapped_pos
                        block, color = selected_block
                        
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            moves_made += 1
                            
                            # Calculate score based on target moves
                            if moves_made > target_moves:
                                score -= 10  # Deduct 10 points for each move beyond target
                            
                            # Add bonus for line/column clears
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            if lines_cleared > 0:
                                score += lines_cleared * 20
                            
                            # Remove used block
                            if selected_index is not None and selected_index < len(blocks):
                                blocks.pop(selected_index)
                                if not blocks:
                                    blocks = LEVEL_BLOCKS[level].copy()
                            
                            hint_block = None  # Clear hint after placement
                            
                            if all(cell == BLACK for row in grid for cell in row):
                                return ("victory", score)
                
                # Reset dragging state
                selected_block = None
                dragging = False
                selected_index = None
                
            # Block rotation (from first code)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                block, color = selected_block
                selected_block = ([list(row) for row in zip(*block[::-1])], color)
                hint_block = None  # Clear hint on rotation

        # Rendering (from second code)
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw hint button (from first code)
        pygame.draw.rect(screen, (100, 70, 30), hint_button, border_radius=5)
        pygame.draw.rect(screen, (50, 30, 10), hint_button, 2, border_radius=5)
        hint_text = button_font.render("DICA", True, (240, 220, 180))
        screen.blit(hint_text, (hint_button.x + 40, hint_button.y + 15))
        
        # Draw hint if available (from first code)
        if hint_block:
            block, color, grid_x, grid_y = hint_block
            hint_surface = pygame.Surface((len(block[0]) * BLOCK_SIZE, len(block) * BLOCK_SIZE), pygame.SRCALPHA)
            
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                        s.fill((color[0], color[1], color[2], hint_alpha))
                        hint_surface.blit(s, (col * BLOCK_SIZE, row * BLOCK_SIZE))
            
            screen.blit(hint_surface, (grid_x * BLOCK_SIZE, grid_y * BLOCK_SIZE))
        
        # Draw dragged block (from second code)
        if dragging and selected_block:
            x, y = pygame.mouse.get_pos()
            block, color = selected_block
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(
                            screen, 
                            color,
                            (x + col * BLOCK_SIZE, 
                             y + row * BLOCK_SIZE,
                             BLOCK_SIZE,
                             BLOCK_SIZE)
                        )
        
        pygame.display.flip()
        clock.tick(60)
    
    return "menu"

def main():
    """
    Main game loop managing state transitions between menus and game modes.
    """
    global current_level, score, game_mode
    
    # Initialize game state and menus
    current_state = "main_menu"
    main_menu = MainMenu(screen)
    game_mode_menu = GameModeMenu(screen)
    level_menu = LevelMenu(screen)
    
    current_algorithm = "greedy"  # Default algorithm
    running = True
    
    while running:
        # State machine for game flow
        if current_state == "main_menu":
            action = main_menu.run()
            if action == "play":
                current_state = "game_mode"
            elif action == "quit":
                running = False
        
        elif current_state == "game_mode":
            action = game_mode_menu.run()
            if action == "human":
                game_mode = "human"
                current_state = "level_select"
            elif action == "pc":
                game_mode = "pc"
                current_state = "algorithm_select"
            elif action == "assistant":
                game_mode = "assistant"
                current_state = "level_select"
            elif action == "back":
                current_state = "main_menu"
        
        elif current_state == "algorithm_select":
            algorithm = show_algorithm_menu(screen)
            if algorithm == "back":
                current_state = "game_mode"
            elif algorithm in ["bfs", "dfs", "greedy", "a_star"]:
                current_algorithm = algorithm
                current_state = "level_select"
        
        elif current_state == "level_select":
            level = level_menu.run()
            if level in [1, 2, 3]:
                current_level = level
                current_state = "game"
            elif level == "back":
                current_state = "game_mode" if game_mode != "pc" else "algorithm_select"
            elif level == "quit":
                running = False
        
        elif current_state == "game":
            # Initialize result with a default value
            result = None
    
            if game_mode == "human":
                result = human_mode(current_level, screen)
            elif game_mode == "pc":
                result = pc_mode(
                    algorithm=current_algorithm,
                    level=current_level,
                    screen=screen,
                    heuristic=combined_heuristic if current_algorithm in ["greedy", "a_star"] else None
                )
            elif game_mode == "assistant":
                result = computer_assisted_human_mode(current_level, screen)
    
            # Only check result if it was set by one of the game modes
            if result is not None:
                if result == "main_menu":
                    current_state = "main_menu"
                elif result == "victory":
                    current_state = "victory"
                elif result == "game_over":
                    current_state = "game_over"
                elif result == "quit":
                    running = False
            else:
                # Handle unexpected case (shouldn't normally happen)
                current_state = "main_menu"
        
        elif current_state == "victory":
            victory = VictoryScreen(screen, score)
            action = victory.run()
            if action == "next_level":
                current_level = 1 if current_level >= 3 else current_level + 1
                current_state = "game"
            elif action == "main_menu":
                current_state = "main_menu"
            elif action == "quit":
                running = False
        
        elif current_state == "game_over":
            game_over = GameOver(screen, score)
            action = game_over.run()
            if action == "retry":
                current_state = "game"
            elif action == "main_menu":
                current_state = "main_menu"
            elif action == "quit":
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()