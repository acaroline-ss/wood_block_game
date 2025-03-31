#main.py
import pygame
import random  
import time 
from render import * 
from cst import * 
from game import *  
from heuristics import *  
from search import * 
from visuals.victory import VictoryScreen
from visuals.levels import show_level_menu
from visuals.game_over import GameOver
from visuals.menu import MainMenu, GameModeMenu, LevelMenu

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
# Define grid sizes for each level
LEVEL_GRID_SIZES = {
    1: 4,  # Level 1: 4x4 grid
    2: 5,  # Level 2: 5x5 grid
    3: 6   # Level 3: 6x6 grid
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
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0]
    ]
}

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
def human_mode(level, screen):
    global selected_block, grid, blocks, score, GRID_SIZE
    
    # Inicializa o nível
    score = 0
    initialize_level(level)
    running = True
    dragging = False
    clock = pygame.time.Clock()
    FPS = 60

    while running:
        # Obter a posição do tabuleiro a cada frame
        board_pos = render(screen, grid, blocks, score, GRID_SIZE)
        # Verificação de vitória (deve vir antes de verificar movimentos)
        if all(cell == BLACK for row in grid for cell in row):
            print("You win! Final Score:", score)
            return ("victory", score)  # Retorna vitória
        
        # Verificação de game over
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            print("No valid moves left! Game Over. Final Score:", score)
            return ("game_over", score)  # Retorna derrota

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Retorna para sair
            
            # Seleção de bloco
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH - 150 <= x <= WIDTH and 50 <= y <= (50 + len(blocks) * 100):
                    selected_index = (y - 50) // 100
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
            
            # Soltar bloco
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_block:
                    x, y = pygame.mouse.get_pos()
                    rel_x = x - board_pos['x']
                    rel_y = y - board_pos['y']
                    snapped_position = snap_to_grid(rel_x, rel_y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    if snapped_position:
                        grid_x, grid_y = snapped_position
                        block, color = selected_block
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            score += lines_cleared * 10
                            
                            blocks.pop(selected_index)
                            if not blocks:
                                blocks = LEVEL_BLOCKS[level].copy()
                            
                            selected_block = None
                    dragging = False
            
            # Rotação
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and selected_block:
                    block, color = selected_block
                    rotated_block = [list(row) for row in zip(*block[::-1])]  # Rotação 90 graus
                    selected_block = (rotated_block, color)

        # Renderização
        render(screen, grid, blocks, score, GRID_SIZE)
        if dragging and selected_block:
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, 
                                        (x + col * BLOCK_SIZE, 
                                         y + row * BLOCK_SIZE, 
                                         BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return "quit"  # Fallback

"""
    Game mode where the computer solves the puzzle using a specified algorithm.
    
    Args:
        algorithm (str): The search algorithm to use ("bfs", "dfs", "greedy", or "a_star").
        heuristic (function): The heuristic function to use (for Greedy or A*).
        level (int): The level to solve (1, 2, or 3).
    """
def pc_mode(algorithm, heuristic=None, level=None):
    global grid, blocks, score
    initialize_level(level)  # Initialize the level

    # Create the initial game state
    initial_state = State([row.copy() for row in grid], blocks.copy())

    # Run the selected search algorithm
    if algorithm == "bfs":
        solution_state = bfs(initial_state, level)
    elif algorithm == "dfs":
        solution_state = dfs(initial_state, level)
    elif algorithm == "greedy":
        solution_state = greedy(initial_state, heuristic, level)
    elif algorithm == "a_star":
        solution_state = a_star(initial_state, heuristic, level)
    else:
        print("Invalid algorithm!")
        return

    if solution_state:  # If a solution is found
        # Visualize the solution path
        current_state = solution_state
        path = []
        while current_state:
            path.append(current_state)
            current_state = current_state.parent  # Traverse the path backward

        # Reverse the path to show from initial to goal state
        for state in reversed(path):
            grid = [row.copy() for row in state.grid]
            blocks = state.blocks.copy()
            score = state.moves * 10  # Update the score based on moves

            # Render the state and delay for visualization
            render(screen, grid, blocks, score, GRID_SIZE)
            pygame.display.flip()
            pygame.time.delay(500)  # Pause for 500ms between states

        print(f"Puzzle solved in {solution_state.moves} moves!")
    else:
        print("No solution found!")


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
        # Use A* to find the next best move
        new_state = a_star(state, combined_heuristic, level)
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
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wood Block Puzzle")
    
    current_state = GameState.MAIN_MENU
    game_mode = None
    selected_level = None
    score = 0

    while True:
        # Menu Principal
        if current_state == GameState.MAIN_MENU:
            menu = MainMenu(screen)
            action = menu.run()
            
            if action == "quit":
                break
            elif action == "play":
                current_state = GameState.GAME_MODE
            elif action == "settings":
                # Implemente suas configurações
                pass
            elif action == "about":
                # Implemente sua tela sobre
                pass

        # Seleção de Modo de Jogo
        elif current_state == GameState.GAME_MODE:
            mode_menu = GameModeMenu(screen)
            action = mode_menu.run()
            
            if action == "back":
                current_state = GameState.MAIN_MENU
            elif action in ["human", "pc", "assistant"]:
                game_mode = action
                current_state = GameState.LEVEL_SELECT

        # Seleção de Nível
        elif current_state == GameState.LEVEL_SELECT:
            level_menu = LevelMenu(screen)
            action = level_menu.run()
            
            if action == "back":
                current_state = GameState.GAME_MODE
            elif action in [1, 2, 3]:
                selected_level = action
                current_state = GameState.GAME

        # Jogo Principal
        elif current_state == GameState.GAME:
            if game_mode == "human":
                result, final_score = human_mode(selected_level, screen)
                
                if result == "game_over":
                    current_state = GameState.GAME_OVER
                    score = final_score
                elif result == "victory":
                    current_state = GameState.VICTORY
                    score = final_score
                elif result == "quit":
                    break

        # Tela de Game Over
        elif current_state == GameState.GAME_OVER:
            game_over = GameOver(screen, score)
            action = game_over.run()
            
            if action == "retry":
                current_state = GameState.GAME
            elif action == "main_menu":
                current_state = GameState.MAIN_MENU
            elif action == "quit":
                break

        # Tela de Vitória
        elif current_state == GameState.VICTORY:
            victory = VictoryScreen(screen, score)
            action = victory.run()
            
            if action == "next_level":
                selected_level = min(3, selected_level + 1)
                current_state = GameState.GAME
            elif action == "main_menu":
                current_state = GameState.MAIN_MENU
            elif action == "quit":
                break

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()