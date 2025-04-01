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

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wood Block Puzzle")
clock = pygame.time.Clock()

# Game state variables
grid = None
blocks = []
selected_block = None
score = 0
current_level = 1
game_mode = None

class GameState:
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
            bg = pygame.image.load("assets/menu_bg.jpg").convert()
            screen.blit(bg, (0, 0))
        except:
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
        
        # Draw background
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
                    
# Define grid sizes for each level
LEVEL_GRID_SIZES = {
    1: 4,  # Level 1: 4x4 grid
    2: 5,  # Level 2: 5x5 grid
    3: 6,  # Level 3: 6x6 grid
    4: 2 # facullll
}

# Pre-filled grids for each level
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
    4: [
        [1, 0],
        [0, 0]
    ]
}

"""
# Initialize Pygame
pygame.init()  # Start the Pygame engine
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)  # Create the game window
pygame.display.set_caption("Wood Block Puzzle")  # Set the window title

# Game state variables
grid = None  # The current game grid (2D list)
blocks = []  # List of blocks available for placement
selected_block = None  # The block currently selected by the player
score = 0  # The player's score
"""

"""
    Initialize the game grid and blocks for a specific level.
    
    Args:
        level (int): The level to initialize (1, 2, or 3).
    """
def initialize_level(level):
    global GRID_SIZE, grid, blocks
    GRID_SIZE = LEVEL_GRID_SIZES[level]  # Set the grid size for the level
    # Create the grid by replacing 1s with random colors and 0s with BLACK
    grid = [[BLACK if cell == 0 else random.choice(COLORS) for cell in row] for row in LEVEL_PRE_FILLED[level]]
    blocks = LEVEL_BLOCKS[level].copy()  # Copy the predefined blocks for the level

"""
    Game mode where a human player interacts with the game.
    
    Args:
        level (int): The level to play (1, 2, or 3).
    """

"""
def human_mode(level):
    global selected_block, grid, blocks, score, GRID_SIZE

    score = 0
    initialize_level(level)
    running = True  # Control the game loop
    dragging = False  # Track if a block is being dragged

    # Configure the clock to control the frame rate (FPS)
    clock = pygame.time.Clock()
    FPS = 60  # Set the frame rate to 60 FPS

    while running:
        # Check if there are any valid moves left
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            print("No valid moves left! Game Over. Final Score:", score)
            running = False
            break

        # Handle events (e.g., mouse clicks, key presses)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user closes the window
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse is clicked
                x, y = pygame.mouse.get_pos()  # Get the mouse position
                # Check if the click is within the block selection area
                if WIDTH - 150 <= x <= WIDTH and 50 <= y <= (50 + len(blocks) * 100):
                    selected_index = (y - 50) // 100  # Calculate which block was clicked
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]  # Select the block
                        dragging = True  # Start dragging the block
            elif event.type == pygame.MOUSEBUTTONUP:  # If the mouse button is released
                if dragging and selected_block:
                    x, y = pygame.mouse.get_pos()  # Get the mouse position
                    # Snap the block to the grid
                    snapped_position = snap_to_grid(x, y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    if snapped_position:  # If the block can be placed
                        grid_x, grid_y = snapped_position  # Get the grid position
                        block, color = selected_block
                        # Check if the block can be placed at the snapped position
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)  # Place the block
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)  # Clear completed lines
                            score += lines_cleared * 10  # Update the score

                            # Remove the used block
                            blocks.pop(selected_index)

                            # If all blocks are used, reload new ones
                            if not blocks:
                                blocks = LEVEL_BLOCKS[level].copy()

                            selected_block = None

                            # Check if the grid is empty (win condition)
                            if all(cell == BLACK for row in grid for cell in row):
                                print("You win! Final Score:", score)
                                running = False
                    else:
                        print("Invalid placement")
                dragging = False  # Stop dragging
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_SPACE and selected_block:  # Rotate the selected block
                    block, color = selected_block
                    rotated_block = list(zip(*block[::-1]))  # Rotate the block 90 degrees
                    selected_block = (rotated_block, color)

        # Render the game
        render(screen, grid, blocks, score, GRID_SIZE)
        if dragging and selected_block:  # If dragging a block, draw it at the mouse position
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()  # Update the display

        # Cap the frame rate
        clock.tick(FPS)

    # Ensure the event queue is processed to prevent freezing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
"""

def human_mode(level, screen):
    global selected_block, grid, blocks, score, GRID_SIZE
    initialize_level(level)
    running = True
    dragging = False
    selected_index = None
    clock = pygame.time.Clock()

    while running:
        # Check game conditions
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            return "game_over"
        if all(cell == BLACK for row in grid for cell in row):
            return "victory"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            # Mouse click - select block
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                x, y = event.pos
                # Check block selection area (right side panel)
                if WIDTH - 150 <= x <= WIDTH and 50 <= y <= 50 + len(blocks) * 100:
                    selected_index = (y - 50) // 100
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
                        
            # Mouse release - place block
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                if selected_block:
                    x, y = pygame.mouse.get_pos()
                    snapped_position = snap_to_grid(x, y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    if snapped_position:
                        grid_x, grid_y = snapped_position
                        block, color = selected_block
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            score += lines_cleared * 10
                            
                            # Remove used block
                            if selected_index is not None and selected_index < len(blocks):
                                blocks.pop(selected_index)
                                if not blocks:  # Repopulate if empty
                                    blocks = LEVEL_BLOCKS[level].copy()
                            
                            # Check win condition
                            if all(cell == BLACK for row in grid for cell in row):
                                return "victory"
                
                selected_block = None
                dragging = False
                selected_index = None
                
            # Rotate block
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and selected_block:
                block, color = selected_block
                rotated_block = [list(row) for row in zip(*block[::-1])]  # Rotate 90°
                selected_block = (rotated_block, color)

        # Rendering
        screen.fill((139, 69, 19))  # Clear with wood background
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw dragged block if dragging
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

"""
    Game mode where the computer solves the puzzle using a specified algorithm.
    
    Args:
        algorithm (str): The search algorithm to use ("bfs", "dfs", "greedy", or "a_star").
        heuristic (function): The heuristic function to use (for Greedy or A*).
        level (int): The level to solve (1, 2, or 3).
    """
def pc_mode(algorithm, level, screen, heuristic=None):
    global grid, blocks, score, GRID_SIZE
    
    # Initialize level and state (same as second code)
    initialize_level(level)
    initial_state = State([row.copy() for row in grid], blocks.copy(), GRID_SIZE)
    
    # Start timing
    start_time = time.time()
    
    # Run algorithm (same as second code)
    if algorithm == "bfs":
        solution_state = bfs(initial_state, level)
    elif algorithm == "dfs":
        solution_state = dfs(initial_state, level)
    elif algorithm == "greedy":
        solution_state = greedy(initial_state, heuristic_filled_cells, level)  # Use heuristic_filled_cells
    elif algorithm == "a_star":
        solution_state = a_star(initial_state, combined_heuristic, level)  # Or heuristic_filled_cells
    else:
        return "game_over"
    
    elapsed_time = time.time() - start_time
    
    if not solution_state:
        return "game_over"
    
    # Reconstruct path (same as second code)
    path = []
    current_state = solution_state
    while current_state:
        path.append(current_state)
        current_state = current_state.parent
    path = path[::-1]  # Reverse to start from initial state

    # Prepare move information (for the right panel)
    move_info = []
    for idx, state in enumerate(path[1:], 1):  # Skip initial state
        if state.action:
            block, color, x, y = state.action
            # Create a small preview of the block (for the move history panel)
            block_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(block_surface, color, (col*10, row*10, 10, 10))
            move_info.append({
                "text": f"Move {idx}: ({x},{y})",
                "block": block_surface
            })
    
    current_move = 0
    clock = pygame.time.Clock()
    
    # Visualization loop (keeps the first code's UI but follows second code's logic)
    while current_move < len(path):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_move < len(path) - 1:
                    current_move += 1  # Next move
                elif event.key == pygame.K_ESCAPE:
                    current_move = len(path) - 1  # Skip to end
        
        # Update game state from path
        state = path[current_move]
        grid = [row.copy() for row in state.grid]
        blocks = state.blocks.copy()
        score = state.moves * 10  # Score based on moves (same as second code)
        
        # Render game (same as first code)
        screen.fill((139, 69, 19))  # Wood background
        render(screen, grid, blocks, score, GRID_SIZE)
        
        # Draw the right-side panel (algorithm info, move history)
        panel_width = 250
        panel_margin = 10
        panel_height = HEIGHT - 20
        panel_x = WIDTH - panel_width - panel_margin
        
        # Panel background
        info_panel = pygame.Rect(panel_x, 10, panel_width, panel_height)
        pygame.draw.rect(screen, (100, 70, 30), info_panel, border_radius=8)
        pygame.draw.rect(screen, (50, 30, 10), info_panel, 2, border_radius=8)
        
        # Draw algorithm info
        y_offset = 20
        title_font = pygame.font.SysFont("Luckiest Guy", 32)
        info_font = pygame.font.SysFont("Arial", 22)
        move_font = pygame.font.SysFont("Arial", 18)
        
        title = title_font.render(f"{algorithm.upper()} Solution", True, (240, 220, 180))
        screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 40
        
        # Game stats
        stats = [
            f"Level: {level}",
            f"Time: {elapsed_time:.2f}s",
            f"Moves: {current_move}/{len(path)-1}",
            f"Score: {score}"
        ]
        
        for text in stats:
            text_surface = info_font.render(text, True, (240, 220, 180))
            screen.blit(text_surface, (panel_x + 15, y_offset))
            y_offset += 30
        
        # Move history (last 4 moves)
        y_offset += 10
        move_title = info_font.render("Move History:", True, (240, 220, 180))
        screen.blit(move_title, (panel_x + 15, y_offset))
        y_offset += 30
        
        if current_move > 0:
            start_idx = max(0, current_move - 4)  # Show last 4 moves
            for i in range(start_idx, current_move):
                move = move_info[i]
                text_surface = move_font.render(move["text"], True, (240, 220, 180))
                screen.blit(text_surface, (panel_x + 15, y_offset))
                screen.blit(move["block"], (panel_x + panel_width - 60, y_offset))
                y_offset += 40
        
        # Controls
        y_offset += 20
        controls_title = info_font.render("Controls:", True, (240, 220, 180))
        screen.blit(controls_title, (panel_x + 15, y_offset))
        y_offset += 30
        
        controls = [
            ("SPACE", "Next move"),
            ("ESC", "Skip to end")
        ]
        
        for key, desc in controls:
            key_text = info_font.render(key, True, (240, 220, 180))
            desc_text = info_font.render(desc, True, (240, 220, 180))
            screen.blit(key_text, (panel_x + 30, y_offset))
            screen.blit(desc_text, (panel_x + 100, y_offset))
            y_offset += 30
        
        pygame.display.flip()
        clock.tick(60)
    
    return "victory"


#TODO IMPLEMENT - ONLY CALLED IF PLAYER WANTS AT ANY POITN IN GAME
"""
    Game mode where the computer provides hints to the human player.
    
    Args:
        level (int): The level to play (1, 2, or 3).
    """
def computer_assisted_human_mode(level=None):
    global grid, blocks
    state = State(grid, blocks)  # Create the initial state
    while not state.is_goal():  # Continue until the goal is reached
        # Use greedy to find the next best move
        new_state = greedy(state, heuristic_filled_cells, level)
        if new_state is None:
            print("No more hints available!")
            return

        # Display the hint
        print("Hint: Place the next block as follows:")
        for row in new_state.grid:
            print(row)
        render(screen, new_state.grid, new_state.blocks, score)
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause for 2 seconds to show the hint

        # Update the state
        state = new_state
        grid = [row[:] for row in state.grid]
        blocks = state.blocks

"""
    Main function to start the game.
    """

"""
def main():
    global grid, blocks
    print("Welcome to Wood Block Puzzle!")
    print("1. Human Mode")
    print("2. PC Mode")
    print("3. Computer-Assisted Human Mode")
    mode = input("Select mode (1/2/3/4): ")
    print("1. Level 1 (4x4 grid)")
    print("2. Level 2 (5x5 grid)")
    print("3. Level 3 (6x6 grid)")
    print("4. Level 4 (2x2 grid)")
    level = int(input("Select level (1/2/3/4): "))

    if level not in LEVEL_BLOCKS:
        print("Invalid level selected.")
        return

    initialize_level(level)  # Initialize the selected level

    if mode == "1":
        human_mode(level)  # Start human mode
    elif mode == "2":
        print("1. BFS")
        print("2. DFS")
        print("3. Greedy")
        print("4. A*")
        algorithm = input("Select algorithm (1/2/3/4): ")
        if algorithm == "1":
            pc_mode("bfs", level=level)
        elif algorithm == "2":
            pc_mode("dfs", level=level)
        elif algorithm == "3":
            pc_mode("greedy", heuristic_filled_cells, level=level)
        elif algorithm == "4":
            pc_mode("a_star", combined_heuristic, level=level)
    elif mode == "3":
        computer_assisted_human_mode(level)  # Start computer-assisted human mode
    pygame.quit()  # Quit Pygame when the game ends

if __name__ == "__main__":
    main()  # Run the main function when the script is executed"
"""

def main():
    global current_level, score, game_mode
    
    current_state = "main_menu"
    main_menu = MainMenu(screen)
    game_mode_menu = GameModeMenu(screen)
    level_menu = LevelMenu(screen)
    
    # Default algorithm for PC mode
    current_algorithm = "greedy"
    running = True
    
    while running:
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
                current_state = "algorithm_select"  # New state for algorithm selection
            elif action == "assistant":
                game_mode = "assistant"
                current_state = "level_select"
            elif action == "back":
                current_state = "main_menu"
        
        # NEW STATE: Algorithm selection for PC mode
        elif current_state == "algorithm_select":
            algorithm = show_algorithm_menu(screen)
            if algorithm == "back":
                current_state = "game_mode"
            elif algorithm in ["bfs", "dfs", "greedy", "a_star"]:
                current_algorithm = algorithm
                current_state = "level_select"
        
        elif current_state == "level_select":
            level = level_menu.run()
            if level in [1, 2, 3, 4]:
                current_level = level
                current_state = "game"
            elif level == "back":
                current_state = "game_mode" if game_mode != "pc" else "algorithm_select"
            elif level == "quit":
                running = False
        
        elif current_state == "game":
            if game_mode == "human":
                result = human_mode(current_level, screen)
            elif game_mode == "pc":
                result = pc_mode(
                    algorithm=current_algorithm,
                    level=current_level,
                    screen=screen,
                    heuristic=combined_heuristic if current_algorithm in ["greedy", "a_star"] else None
                )
            #elif game_mode == "assistant":
                #result = assistant_mode(current_level, screen)  # Implement this if needed
            
            if result == "victory":
                current_state = "victory"
            elif result == "game_over":
                current_state = "game_over"
            elif result == "quit":
                running = False
        
        elif current_state == "victory":
            victory = VictoryScreen(screen, score)
            action = victory.run()
            if action == "next_level":
                current_level += 1
                if current_level > 4:  # Wrap around if max level reached
                    current_level = 1
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