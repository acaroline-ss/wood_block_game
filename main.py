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
from visuals.assets import *
from visuals.buttons import *

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wood Block Puzzle")
clock = pygame.time.Clock()

# Game state variables
grid = None          # Current game grid (2D list of colors)
blocks = []          # Available blocks to place
selected_block = None  # Currently selected/dragged block
score = 0            # Player's current score
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
    """
    Display the main menu and handle user input.
    
    Args:
        screen (pygame.Surface): The game window surface.
    
    Returns:
        str: The action to take ("quit" or GameState constant).
    """
    font = pygame.font.SysFont("Luckiest Guy", 48)
    buttons = [
        {"text": "Jogar", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "action": GameState.LEVEL_SELECTION},
        {"text": "Sair", "rect": pygame.Rect(WIDTH//2-100, 280, 200, 50), "action": "quit"}
    ]
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw background (fallback to solid color if image fails)
        try:
            bg = pygame.image.load("assets/menu_bg.jpg").convert()
            screen.blit(bg, (0, 0))
        except:
            screen.fill((139, 69, 19))  # Fallback brown color
        
        # Draw title
        title = font.render("Wood Block Puzzle", True, (240, 220, 180))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw and handle buttons
        for btn in buttons:
            # Highlight button on hover
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
    """
    Display algorithm selection menu for PC mode.
    
    Args:
        screen (pygame.Surface): The game window surface.
    
    Returns:
        str: Selected algorithm or "back" to return.
    """
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
        screen.fill((139, 69, 19))  # Wood background
        
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

# Level configuration
LEVEL_CONFIG = {
    1: {
        "size": 4,
        "grid": [
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]
        ]
    },
    2: {
        "size": 5,
        "grid": [
            [1, 0, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 1, 0]
        ]
    },
    3: {
        "size": 6,
        "grid": [
            [1, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0]
        ]
    },
}

def initialize_level(level):
    """
    Initialize game state for a specific level.
    
    Args:
        level (int): The level number (1-4) to initialize.
    """
    global GRID_SIZE, grid, blocks
    
    config = LEVEL_CONFIG.get(level, LEVEL_CONFIG[1])  # Default to level 1 if invalid
    GRID_SIZE = config["size"]
    
    # Convert 1s to random colors and 0s to BLACK
    grid = [[BLACK if cell == 0 else random.choice(COLORS) 
             for cell in row] 
             for row in config["grid"]]
    
    blocks = LEVEL_BLOCKS[level].copy()  # Create a fresh copy of blocks

def human_mode(level, screen):
    """
    Human player game mode.
    
    Args:
        level (int): The level to play.
        screen (pygame.Surface): The game window surface.
    
    Returns:
        str: Next game state ("victory", "game_over", "quit", or "menu").
    """
    global selected_block, grid, blocks, score, GRID_SIZE
    
    initialize_level(level)
    running = True
    dragging = False
    selected_index = None

    while running:
        # Game state checks
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            return "game_over"
        if all(cell == BLACK for row in grid for cell in row):
            return "victory"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Block selection
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if WIDTH - 150 <= x <= WIDTH and 50 <= y <= 50 + len(blocks) * 100:
                    selected_index = (y - 50) // 100
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
                        
            # Block placement
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                if selected_block:
                    x, y = pygame.mouse.get_pos()
                    snapped_pos = snap_to_grid(x, y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    
                    if snapped_pos:
                        grid_x, grid_y = snapped_pos
                        block, color = selected_block
                        
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            score += clear_completed_lines(grid, GRID_SIZE) * 10
                            
                            # Remove used block and check if need to repopulate
                            if selected_index is not None and selected_index < len(blocks):
                                blocks.pop(selected_index)
                                if not blocks:
                                    blocks = LEVEL_BLOCKS[level].copy()
                            
                            if all(cell == BLACK for row in grid for cell in row):
                                return "victory"
                
                # Reset dragging state
                selected_block = None
                dragging = False
                selected_index = None
                
            # Block rotation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                block, color = selected_block
                # Rotate 90 degrees clockwise
                selected_block = ([list(row) for row in zip(*block[::-1])], color)

        # Rendering
        screen.fill((139, 69, 19))
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw dragged block
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

def pc_mode(algorithm, level, screen, heuristic=None):
    """
    Computer-controlled game mode using specified algorithm.
    
    Args:
        algorithm (str): Search algorithm to use ("bfs", "dfs", "greedy", "a_star").
        level (int): The level to solve.
        screen (pygame.Surface): The game window surface.
        heuristic (function, optional): Heuristic function for informed searches.
    
    Returns:
        str: Next game state ("menu", "victory", "game_over", or "quit").
    """
    global grid, blocks, score, GRID_SIZE
    
    initialize_level(level)
    initial_state = State([row.copy() for row in grid], blocks.copy(), GRID_SIZE)
    
    # Time the algorithm execution
    start_time = time.time()
    
    # Run selected algorithm
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

    # Prepare move information for display
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
    menu_button = Button("MENU", (20, HEIGHT - 70), "main_menu")
    
    # Visualization loop
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
        score = state.moves * 10
        
        # Render game
        screen.fill((139, 69, 19))
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw menu button
        menu_button.draw(screen)
        
        # Draw info panel on right
        panel_width = 250
        panel_x = WIDTH - panel_width - 10
        info_panel = pygame.Rect(panel_x, 10, panel_width, HEIGHT - 20)
        
        # Panel background
        pygame.draw.rect(screen, (100, 70, 30), info_panel, border_radius=8)
        pygame.draw.rect(screen, (50, 30, 10), info_panel, 2, border_radius=8)
        
        # Draw algorithm info
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
    Human player mode with computer hints.
    
    Args:
        level (int): The level to play.
        screen (pygame.Surface): The game window surface.
    
    Returns:
        str: Next game state ("victory", "game_over", "quit", or "menu").
    """
    global selected_block, grid, blocks, score, GRID_SIZE
    
    initialize_level(level)
    running = True
    dragging = False
    selected_index = None
    hint_block = None
    hint_alpha = 100  # Hint transparency

    # Hint button setup
    hint_button = pygame.Rect(WIDTH - 150, HEIGHT - 70, 120, 50)
    button_font = pygame.font.SysFont("Arial", 24)

    while running:
        # Game state checks
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            return "game_over"
        if all(cell == BLACK for row in grid for cell in row):
            return "victory"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Hint button or block selection
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                
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
                
                # Block selection
                elif WIDTH - 150 <= x <= WIDTH and 50 <= y <= 50 + len(blocks) * 100:
                    selected_index = (y - 50) // 100
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
                        hint_block = None  # Clear hint on new selection
                        
            # Block placement
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                if selected_block:
                    x, y = pygame.mouse.get_pos()
                    snapped_pos = snap_to_grid(x, y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    
                    if snapped_pos:
                        grid_x, grid_y = snapped_pos
                        block, color = selected_block
                        
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            score += clear_completed_lines(grid, GRID_SIZE) * 10
                            
                            # Remove used block
                            if selected_index is not None and selected_index < len(blocks):
                                blocks.pop(selected_index)
                                if not blocks:
                                    blocks = LEVEL_BLOCKS[level].copy()
                            
                            hint_block = None  # Clear hint after placement
                            
                            if all(cell == BLACK for row in grid for cell in row):
                                return "victory"
                
                # Reset dragging state
                selected_block = None
                dragging = False
                selected_index = None
                
            # Block rotation
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                block, color = selected_block
                selected_block = ([list(row) for row in zip(*block[::-1])], color)
                hint_block = None  # Clear hint on rotation

        # Rendering
        screen.fill((139, 69, 19))
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw hint button
        pygame.draw.rect(screen, (100, 70, 30), hint_button, border_radius=5)
        pygame.draw.rect(screen, (50, 30, 10), hint_button, 2, border_radius=5)
        hint_text = button_font.render("DICA", True, (240, 220, 180))
        screen.blit(hint_text, (hint_button.x + 40, hint_button.y + 15))
        
        # Draw hint if available
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
        
        # Draw dragged block
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