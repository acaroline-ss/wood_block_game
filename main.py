import pygame
import random
from collections import deque
import heapq
import time
from render import *
from cst import *
from game import *
from heuristics import *
from search import *

# Define grid sizes for each level
LEVEL_GRID_SIZES = {
    1: 4,  # Level 1: 4x4 grid
    2: 5,  # Level 2: 5x5 grid
    3: 6   # Level 3: 6x6 grid
}

# Pre-filled grids for each level
LEVEL_PRE_FILLED = {
    1: [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ],
    2: [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0]
    ],
    3: [
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0]
    ]
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wood Block Puzzle")

# Game state
grid = None
blocks = []
selected_block = None
score = 0

def initialize_level(level):
    """Initialize the grid and blocks for the selected level."""
    global GRID_SIZE, grid, blocks
    GRID_SIZE = LEVEL_GRID_SIZES[level]  # Update GRID_SIZE based on the selected level
    grid = [[BLACK if cell == 0 else random.choice(COLORS) for cell in row] for row in LEVEL_PRE_FILLED[level]]
    blocks = [generate_block(level) for _ in range(3)]


# main.py
def human_mode(level):
    global selected_block, grid, blocks, score, GRID_SIZE
    running = True
    dragging = False

    # Configura o clock para controlar a taxa de quadros (FPS)
    clock = pygame.time.Clock()
    FPS = 60  # Define a taxa de quadros para 60 FPS

    while running:
        # Verifica se há movimentos válidos restantes
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            print("No valid moves left! Game Over. Final Score:", score)
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH - 150 <= x <= WIDTH - 50 and 50 <= y <= 350:
                    selected_index = (y - 50) // 100
                    selected_block = blocks[selected_index]
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_block:
                    x, y = pygame.mouse.get_pos()
                    # Ajusta a posição para o centro da célula mais próxima com snap-to-grid
                    snapped_position = snap_to_grid(x, y, selected_block[0], grid, GRID_SIZE)
                    if snapped_position:  # Verifica se a posição ajustada é válida
                        grid_x, grid_y = snapped_position
                        block, color = selected_block
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):  # Tolerância de 2 células
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            score += lines_cleared * 10

                            # Remove o bloco usado
                            blocks.pop(selected_index)

                            # Recarrega novos blocos se necessário
                            if not blocks:
                                blocks = [generate_block(level) for _ in range(3)]

                            selected_block = None

                            # Verifica se o grid está vazio (condição de vitória)
                            if all(cell == BLACK for row in grid for cell in row):
                                print("You win! Final Score:", score)
                                running = False
                        else:
                            print("Posição inválida: sobreposição detectada!")  # Feedback no console
                    else:
                        print("Posição inválida: fora do grid ou sobreposição!")  # Feedback no console
                    dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and selected_block:
                    block, color = selected_block
                    rotated_block = list(zip(*block[::-1]))  # Rotaciona o bloco 90 graus
                    selected_block = (rotated_block, color)

        # Renderiza o jogo
        screen.fill(WHITE)  # Limpa a tela com a cor de fundo
        render(screen, grid, blocks, score, GRID_SIZE)

        # Renderiza a peça sendo arrastada
        if dragging and selected_block:
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()  # Atualiza a tela
        clock.tick(FPS)  # Mantém a taxa de quadros constante


def pc_mode(algorithm, heuristic=None):
    """PC mode where the computer solves the puzzle."""
    global grid, blocks
    state = State(grid, blocks)
    start_time = time.time()
    visited_states = 0

    while not state.is_goal():
        if algorithm == "bfs":
            new_state = bfs(state)
        elif algorithm == "dfs":
            new_state = dfs(state)
        elif algorithm == "greedy":
            new_state = greedy(state, heuristic)
        elif algorithm == "a_star":
            new_state = a_star(state, heuristic)

        if new_state is None:
            print("No solution found!")
            return

        state = new_state
        grid = [row[:] for row in state.grid]
        blocks = state.blocks

        visited_states += 1
        print(f"Visited states: {visited_states}")
        print(f"Remaining blocks: {len(state.blocks)}")
        print("Current grid:")
        for row in state.grid:
            print(row)

        render(screen, state.grid, state.blocks, score)
        pygame.time.delay(500)

    print(f"Puzzle solved in {time.time() - start_time:.2f} seconds!")
    print(f"Visited states: {visited_states}")

def computer_assisted_human_mode():
    """Computer-assisted human mode where the computer gives hints."""
    global grid, blocks
    state = State(grid, blocks)
    while not state.is_goal():
        # Use A* to find the next best move
        new_state = a_star(state, combined_heuristic_empty_grid)
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

def main():
    """Main function to start the game."""
    global grid, blocks
    print("Welcome to Wood Block Puzzle!")
    print("1. Human Mode")
    print("2. PC Mode")
    print("3. Computer-Assisted Human Mode")
    mode = input("Select mode (1/2/3): ")
    print("1. Level 1 (4x4 grid)")
    print("2. Level 2 (5x5 grid)")
    print("3. Level 3 (6x6 grid)")
    level = int(input("Select level (1/2/3): "))
    initialize_level(level)

    if mode == "1":
        human_mode(level)  # Pass the level to human_mode
    elif mode == "2":
        print("1. BFS")
        print("2. DFS")
        print("3. Greedy")
        print("4. A*")
        algorithm = input("Select algorithm (1/2/3/4): ")
        if algorithm == "1":
            pc_mode("bfs")
        elif algorithm == "2":
            pc_mode("dfs")
        elif algorithm == "3":
            pc_mode("greedy", heuristic_filled_cells)
        elif algorithm == "4":
            pc_mode("a_star", combined_heuristic_empty_grid)
    elif mode == "3":
        computer_assisted_human_mode()
    pygame.quit()

if __name__ == "__main__":
    main()
