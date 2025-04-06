"""
Wood Block Puzzle Game

A puzzle game where players place colored blocks on a grid to complete lines.
Features multiple game modes (human vs computer, computer solver, assisted play)
and search algorithms (BFS, DFS, Greedy, A*).

Game Components:
- Grid system with colored blocks
- Multiple levels with increasing difficulty
- Score system with bonuses and penalties
- Visual feedback and animations

Modules:
- render.py: Handles graphics rendering
- cst.py: Contains game constants
- game.py: Core game logic
- heuristics.py: AI heuristic functions  
- search.py: Search algorithms
- visuals/: UI components and menus
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

# Ensure Python looks for files in the project root
PROJECT_ROOT = Path(__file__).parent
os.chdir(PROJECT_ROOT)
sys.path.append(str(PROJECT_ROOT))

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wood Block Puzzle")
clock = pygame.time.Clock()

# Game state variables
grid = None          # 2D list representing the game board
blocks = []          # Available blocks for placement
selected_block = None  # Currently selected block
score = 100          # Player score (starts at 100)
current_level = 1    # Current level (1-3)
game_mode = None     # Active game mode

class GameState:
    """Enumeration of possible game states"""
    MAIN_MENU = 0
    GAME_MODE = 1
    LEVEL_SELECT = 2
    GAME = 3
    GAME_OVER = 4
    VICTORY = 5

def show_main_menu(screen):
    """Display the main menu and handle user input.
    
    Args:
        screen: Pygame display surface
        
    Returns:
        str: Action to take ("quit" or GameState constant)
    """
    font = pygame.font.SysFont("Luckiest Guy", 48)
    buttons = [
        {"text": "Play", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "action": GameState.LEVEL_SELECTION},
        {"text": "Quit", "rect": pygame.Rect(WIDTH//2-100, 280, 200, 50), "action": "quit"}
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw background with fallback
        try:
            bg = pygame.image.load(MENU_ASSETS["main_bg"]).convert()
            screen.blit(bg, (0, 0))
        except Exception as e:
            print(f"Error loading background: {e}")
            screen.fill((139, 69, 19))  # Fallback color
        
        # Draw title and buttons
        title = font.render("Wood Block Puzzle", True, (240, 220, 180))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        for btn in buttons:
            color = (100, 70, 30) if btn["rect"].collidepoint(mouse_pos) else (70, 40, 10)
            pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
            pygame.draw.rect(screen, (50, 30, 10), btn["rect"], 2, border_radius=8)
            
            btn_text = font.render(btn["text"], True, (240, 220, 180))
            screen.blit(btn_text, btn_text.get_rect(center=btn["rect"].center))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return btn["action"]

def show_algorithm_menu(screen):
    """Display algorithm selection menu for computer mode.
    
    Args:
        screen: Pygame display surface
        
    Returns:
        str: Selected algorithm or "back"/"quit"
    """
    font = pygame.font.SysFont("Luckiest Guy", 36)
    buttons = [
        {"text": "BFS", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "action": "bfs"},
        {"text": "DFS", "rect": pygame.Rect(WIDTH//2-100, 270, 200, 50), "action": "dfs"},
        {"text": "Greedy", "rect": pygame.Rect(WIDTH//2-100, 340, 200, 50), "action": "greedy"},
        {"text": "A*", "rect": pygame.Rect(WIDTH//2-100, 410, 200, 50), "action": "a_star"},
        {"text": "Back", "rect": pygame.Rect(WIDTH//2-100, 480, 200, 50), "action": "back"}
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw menu
        try:
            bg = pygame.image.load(MENU_ASSETS["main_bg"]).convert()
            screen.blit(bg, (0, 0))
        except Exception as e:
            print(f"Error loading background: {e}")
            screen.fill((139, 69, 19))
        
        title = pygame.font.SysFont("Luckiest Guy", 48).render(
            "Select Algorithm", True, (240, 220, 180))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        for btn in buttons:
            color = (100, 70, 30) if btn["rect"].collidepoint(mouse_pos) else (70, 40, 10)
            pygame.draw.rect(screen, color, btn["rect"], border_radius=8)
            pygame.draw.rect(screen, (50, 30, 10), btn["rect"], 2, border_radius=8)
            
            btn_text = font.render(btn["text"], True, (240, 220, 180))
            screen.blit(btn_text, btn_text.get_rect(center=btn["rect"].center))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        return btn["action"]

# Level configurations
LEVEL_CONFIG = {
    1: {"size": 4, "grid": [[1, 0, 0, 0], [1, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]]},
    2: {"size": 5, "grid": [[1, 0, 0, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 1, 0], 
                           [0, 0, 1, 1, 0], [0, 0, 1, 1, 0]]},
    3: {"size": 6, "grid": [[1, 1, 0, 0, 0, 0], [1, 1, 0, 1, 1, 1], [0, 0, 0, 0, 0, 1],
                           [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 0], [0, 1, 0, 0, 0, 0]]}
}

def initialize_level(level):
    """Set up game state for a specific level.
    
    Args:
        level (int): Level number (1-3)
    """
    global GRID_SIZE, grid, blocks, target_moves, moves_made
    
    config = LEVEL_CONFIG.get(level, LEVEL_CONFIG[1])
    GRID_SIZE = config["size"]
    
    # Initialize grid with random colors for pre-filled cells
    grid = [[BLACK if cell == 0 else random.choice(COLORS) 
            for cell in row] 
            for row in config["grid"]]
    
    blocks = LEVEL_BLOCKS[level].copy()
    target_moves = {1: 5, 2: 12, 3: 44}.get(level, 5)
    moves_made = 0
    score = 100

def human_mode(level, screen):
    """Human player game mode.
    
    Args:
        level (int): Current level
        screen: Pygame display surface
        
    Returns:
        tuple: (result state, score) or "quit"
    """
    global selected_block, grid, blocks, score, moves_made
    
    initialize_level(level)
    dragging = False
    selected_index = None
    
    while True:
        # Game state checks
        if all(cell == BLACK for row in grid for cell in row):
            return ("victory", score)
        if no_valid_moves_left(grid, blocks, GRID_SIZE) or score <= 0:
            return ("game_over", score)

        board_pos = render(screen, grid, blocks, score, GRID_SIZE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Block selection
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if HEIGHT-120 <= y <= HEIGHT:  # Click in blocks panel
                    selected_index = (x - (WIDTH - len(blocks)*120)//2) // 120
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
            
            # Block placement
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                if selected_block:
                    rel_x, rel_y = event.pos[0]-board_pos['x'], event.pos[1]-board_pos['y']
                    if (snapped_pos := snap_to_grid(rel_x, rel_y, selected_block[0], grid, GRID_SIZE, 20)):
                        grid_x, grid_y = snapped_pos
                        block, color = selected_block
                        
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, 2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            moves_made += 1
                            
                            # Score calculation
                            if moves_made > target_moves:
                                score -= 20
                            
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            if moves_made > target_moves and lines_cleared:
                                score += 20 + lines_cleared * 10
                            
                            blocks.pop(selected_index)
                            if not blocks:
                                blocks = LEVEL_BLOCKS[level].copy()
                
                selected_block = None
                dragging = False
                selected_index = None
                
            # Block rotation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                block, color = selected_block
                selected_block = ([list(row) for row in zip(*block[::-1])], color)

        # Rendering
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw dragged block
        if dragging and selected_block:
            x, y = pygame.mouse.get_pos()
            block, color = selected_block
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, 
                                       (x + col*BLOCK_SIZE, y + row*BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.display.flip()
        clock.tick(60)

def pc_mode(algorithm, level, screen, heuristic=None):
    """Computer solver mode with visualization.
    
    Args:
        algorithm (str): Search algorithm to use
        level (int): Current level
        screen: Pygame display surface
        heuristic (function): Optional heuristic function
        
    Returns:
        str: Result state ("victory", "game_over", "quit")
    """
    global grid, blocks
    
    initialize_level(level)
    initial_state = State([row.copy() for row in grid], blocks.copy(), GRID_SIZE)
    
    # Algorithm selection
    algorithms = {
        "bfs": lambda s: bfs(s, level),
        "dfs": lambda s: dfs(s, level),
        "greedy": lambda s: greedy(s, heuristic_filled_cells, level),
        "a_star": lambda s: a_star(s, combined_heuristic, level)
    }
    
    start_time = time.time()
    solution_state = algorithms.get(algorithm)(initial_state)
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

    # Prepare move visualization
    move_info = []
    for idx, state in enumerate(path[1:], 1):
        if state.action:
            block, color, x, y = state.action
            block_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(block_surface, color, (col*10, row*10, 10, 10))
            move_info.append({"text": f"Move {idx}: ({x},{y})", "block": block_surface})

    menu_button = Button("MENU", (150, HEIGHT - 70), "main_menu")
    current_move = 0
    
    # Visualization loop
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
            if menu_button.handle_event(event):
                return menu_button.action
        
        # Update state from current move
        state = path[current_move]
        grid = [row.copy() for row in state.grid]
        blocks = state.blocks.copy()
        
        # Render game
        screen.fill((139, 69, 19))
        render(screen, grid, [], 0, GRID_SIZE)  # Hide bottom blocks
        menu_button.draw(screen)
        
        # Draw info panel
        panel_width = 250
        panel_x = WIDTH - panel_width - 10
        pygame.draw.rect(screen, (100, 70, 30), (panel_x, 10, panel_width, HEIGHT-20), border_radius=8)
        pygame.draw.rect(screen, (50, 30, 10), (panel_x, 10, panel_width, HEIGHT-20), 2, border_radius=8)
        
        # Draw algorithm info
        y_offset = 20
        fonts = {
            "title": pygame.font.SysFont("Luckiest Guy", 28),
            "info": pygame.font.SysFont("Arial", 20, bold=True),
            "move": pygame.font.SysFont("Arial", 16, bold=True)
        }
        
        title = fonts["title"].render(f"{algorithm.upper()} Solution", True, (240, 220, 180))
        screen.blit(title, (panel_x + (panel_width - title.get_width())//2, y_offset))
        y_offset += 40
        
        for text in [f"Level: {level}", f"Time: {elapsed_time:.2f}s", f"Moves: {current_move}/{len(path)-1}"]:
            text_surface = fonts["info"].render(text, True, (240, 220, 180))
            screen.blit(text_surface, (panel_x + 15, y_offset))
            y_offset += 30
        
        # Move history
        if current_move > 0:
            y_offset += 10
            move_title = fonts["info"].render("Move History:", True, (240, 220, 180))
            screen.blit(move_title, (panel_x + 15, y_offset))
            y_offset += 30
            
            for i in range(max(0, current_move-4), current_move):
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
            screen.blit(fonts["move"].render(key, True, (240, 220, 180)), (panel_x + 30, y_offset))
            screen.blit(fonts["move"].render(desc, True, (240, 220, 180)), (panel_x + 100, y_offset))
            y_offset += 30
        
        pygame.display.flip()
        clock.tick(60)
    
    return "victory"

def computer_assisted_human_mode(level, screen):
    """Human mode with computer hints.
    
    Args:
        level (int): Current level
        screen: Pygame display surface
        
    Returns:
        tuple: (result state, score) or "quit"
    """
    global selected_block, grid, blocks, score, moves_made
    
    initialize_level(level)
    dragging = False
    selected_index = None
    hint_block = None
    hint_button = pygame.Rect(WIDTH - 150, HEIGHT - 70, 120, 50)
    
    while True:
        # Game state checks
        if no_valid_moves_left(grid, blocks, GRID_SIZE) or score <= 0:
            return ("game_over", score)
        if all(cell == BLACK for row in grid for cell in row):
            return ("victory", score)

        board_pos = render(screen, grid, blocks, score, GRID_SIZE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Hint button or block selection
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                if hint_button.collidepoint(x, y):
                    score -= 30  # Hint cost
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
                            hint_block = (*path[0].action,)
                
                # Block selection
                elif HEIGHT-120 <= y <= HEIGHT:
                    selected_index = (x - (WIDTH - len(blocks)*120)//2) // 120
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
                        hint_block = None
                        
            # Block placement
            elif event.type == pygame.MOUSEBUTTONUP and dragging:
                if selected_block:
                    rel_x, rel_y = event.pos[0]-board_pos['x'], event.pos[1]-board_pos['y']
                    if (snapped_pos := snap_to_grid(rel_x, rel_y, selected_block[0], grid, GRID_SIZE, 20)):
                        grid_x, grid_y = snapped_pos
                        block, color = selected_block
                        
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, 2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            moves_made += 1
                            
                            if moves_made > target_moves:
                                score -= 20
                            
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            if lines_cleared and moves_made > target_moves:
                                score += 20 + lines_cleared * 10
                            
                            blocks.pop(selected_index)
                            if not blocks:
                                blocks = LEVEL_BLOCKS[level].copy()
                            
                            hint_block = None
                
                selected_block = None
                dragging = False
                selected_index = None
                
            # Block rotation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                selected_block = ([list(row) for row in zip(*selected_block[0][::-1])], selected_block[1])
                hint_block = None

        # Rendering
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw hint button
        pygame.draw.rect(screen, (100, 70, 30), hint_button, border_radius=5)
        pygame.draw.rect(screen, (50, 30, 10), hint_button, 2, border_radius=5)
        hint_text = pygame.font.SysFont("Arial", 24).render("HINT (-30)", True, (240, 220, 180))
        screen.blit(hint_text, (hint_button.x + 20, hint_button.y + 15))
        
        # Draw hint
        if hint_block:
            block, color, grid_x, grid_y = hint_block
            hint_surface = pygame.Surface((len(block[0])*BLOCK_SIZE, len(block)*BLOCK_SIZE), pygame.SRCALPHA)
    
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                        s.fill((*color, 100))  # Semi-transparent
                        hint_surface.blit(s, (col*BLOCK_SIZE, row*BLOCK_SIZE))
    
            screen.blit(hint_surface, (
                board_pos['x'] + grid_x*BLOCK_SIZE, 
                board_pos['y'] + grid_y*BLOCK_SIZE
            ))
        
        # Draw dragged block
        if dragging and selected_block:
            x, y = pygame.mouse.get_pos()
            block, color = selected_block
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, 
                                       (x + col*BLOCK_SIZE, y + row*BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.display.flip()
        clock.tick(60)

def main():
    """Main game loop managing state transitions."""
    global current_level, score, game_mode
    
    # Initialize game state
    current_state = "main_menu"
    main_menu = MainMenu(screen)
    game_mode_menu = GameModeMenu(screen)
    level_menu = LevelMenu(screen)
    current_algorithm = "greedy"
    
    while True:
        # State machine
        if current_state == "main_menu":
            action = main_menu.run()
            if action == "play":
                current_state = "game_mode"
            elif action == "quit":
                break
        
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
                break
        
        elif current_state == "game":
            score = 100  # Reset score
            
            # Run appropriate game mode
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

            # Handle result
            if isinstance(result, tuple):
                result_state, result_score = result
                score = result_score
                current_state = "victory" if result_state == "victory" else "game_over"
            elif result == "victory":
                current_state = "victory"
            elif result == "game_over":
                current_state = "game_over"
            elif result == "quit":
                break
            elif result == "main_menu":
                current_state = "main_menu"
        
        elif current_state == "victory":
            action = VictoryScreen(screen, score).run()
            if action == "next_level":
                current_level = min(3, current_level + 1)
                current_state = "game"
            elif action == "main_menu":
                current_state = "main_menu"
            elif action == "quit":
                break
        
        elif current_state == "game_over":
            action = GameOver(screen, score).run()
            if action == "retry":
                current_state = "game"
            elif action == "main_menu":
                current_state = "main_menu"
            elif action == "quit":
                break
    
    pygame.quit()

if __name__ == "__main__":
    main()