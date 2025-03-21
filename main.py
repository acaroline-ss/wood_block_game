""""
import pygame
import random
from collections import deque
import heapq
import time
from render import *
from cst import *
#import game
from game import *
from heuristics import *
from search import *

# Grid settings
GRID_SIZE = None  # Will be set based on the level
BLOCK_SIZE = 40  # Size of each grid cell
WIDTH = 600  # Window width
HEIGHT = 600  # Window height

#TODO MOVE TO CST ?
# Define grid sizes for each level
LEVEL_GRID_SIZES = {
    1: 4,  # Level 1: 4x4 grid
    2: 5,  # Level 2: 5x5 grid
    3: 6   # Level 3: 6x6 grid
}

#TODO MOVE TO CST ??
# Pre-filled grids for each level
LEVEL_PRE_FILLED = {
    1: [
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    2: [
        [1, 1, 0, 0, 0],
        [1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1]
    ],
    3: [
        [1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0]
    ]
}

# Game modes
def pc_mode(algorithm, heuristic=None):
    global grid, blocks
    state = State(grid, blocks)  # Cria o estado inicial
    grid, blocks = place_random_block(grid, blocks)  # Coloca um bloco aleatório para iniciar
    start_time = time.time()  # Inicia o cronômetro
    visited_states = 0  # Contador de estados visitados

    while not state.is_goal():  # Enquanto o estado atual não for o objetivo
        if algorithm == "bfs":
            new_state = bfs(state)  # Executa BFS
        elif algorithm == "dfs":
            new_state = dfs(state)  # Executa DFS
        elif algorithm == "greedy":
            new_state = greedy(state, heuristic)  # Executa Greedy
        elif algorithm == "a_star":
            new_state = a_star(state, heuristic)  # Executa A*

        if new_state is None:  # Se nenhum estado válido for encontrado
            print("No solution found!")
            return

        state = new_state  # Atualiza o estado atual
        grid = [row[:] for row in state.grid]  # Atualiza a grid
        blocks = state.blocks  # Atualiza os blocos

        visited_states += 1  # Incrementa o contador de estados visitados
        print(f"Visited states: {visited_states}")  # Exibe o número de estados visitados
        print(f"Remaining blocks: {len(state.blocks)}")  # Exibe o número de blocos restantes
        print("Current grid:")  # Exibe a grade atual
        for row in state.grid:
            print(row)

        render(screen, state.grid, state.blocks, score)  # Renderiza a interface gráfica
        pygame.time.delay(500)  # Pausa de 500ms para visualização

    print(f"Puzzle solved in {time.time() - start_time:.2f} seconds!")  # Exibe o tempo total
    print(f"Visited states: {visited_states}")  # Exibe o número total de estados visitados


def human_mode():
    global selected_block, grid, blocks, score
    running = True  # Controla o loop principal do jogo
    dragging = False  # Indica se um bloco está sendo arrastado

    while running:  # Loop principal do jogo
        for event in pygame.event.get():  # Processa eventos do Pygame
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Se o botão do mouse for pressionado
                x, y = pygame.mouse.get_pos()
                # Verifica se o clique foi na área dos blocos disponíveis
                if WIDTH - 150 <= x <= WIDTH - 50 and 50 <= y <= 350:
                    selected_index = (y - 50) // 100  # Calcula o índice do bloco selecionado
                    selected_block = blocks[selected_index]  # Seleciona o bloco
                    dragging = True  # Inicia o arrasto
            elif event.type == pygame.MOUSEBUTTONUP:  # Se o botão do mouse for solto
                if dragging and selected_block:  # Se um bloco estava sendo arrastado
                    x, y = pygame.mouse.get_pos()
                    grid_x, grid_y = x // BLOCK_SIZE, y // BLOCK_SIZE  # Converte a posição do mouse para coordenadas da grade
                    block, color = selected_block
                    if can_place_block(block, grid_x, grid_y, grid):  # Verifica se o bloco pode ser colocado
                        place_block(block, grid_x, grid_y, color, grid)  # Coloca o bloco na grade
                        lines_cleared = clear_completed_lines(grid)  # Limpa linhas completas
                        score += lines_cleared * 10  # Atualiza a pontuação
                        blocks[selected_index] = generate_block()  # Gera um novo bloco
                        selected_block = None  # Deseleciona o bloco
                        if all(cell == BLACK for row in grid for cell in row):  # Verifica se a grade está cheia
                            print("You win! Final Score:", score)
                            running = False
                    dragging = False  # Finaliza o arrasto
            elif event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if event.key == pygame.K_SPACE:  # Se a tecla for espaço
                    if selected_block:  # Rotaciona o bloco selecionado
                        block, color = selected_block
                        rotated_block = list(zip(*block[::-1]))  # Rotaciona 90 graus
                        selected_block = (rotated_block, color)

        # Verifica se não há mais movimentos válidos
        if no_valid_moves_left(grid, blocks):
            print("No valid moves left! Game Over. Final Score:", score)
            running = False

        render(screen, grid, blocks, score)  # Renderiza a interface gráfica
        # Desenha o bloco selecionado sendo arrastado
        if dragging and selected_block:
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            # Desenha o bloco na posição do mouse
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()  # Atualiza a tela


# Main function
def main():
    print("Welcome to Wood Block Puzzle!")
    global GRID_SIZE, grid, blocks

    # Ask for mode (Human or PC)
    print("1. Human Mode")
    print("2. PC Mode")
    mode = input("Select mode (1/2): ")

    # Ask for level (1, 2, or 3)
    print("1. Level 1 (4x4 grid)")
    print("2. Level 2 (5x5 grid)")
    print("3. Level 3 (6x6 grid)")
    level = int(input("Select level (1/2/3): "))
    GRID_SIZE = LEVEL_GRID_SIZES[level]  # Set grid size based on level
    grid = [[BLACK for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Initialize grid

    if mode == "1":  # Human Mode
        human_mode()
    elif mode == "2":  # PC Mode
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
    pygame.quit()  # Encerra o Pygame

if __name__ == "__main__":
    main()
    
    
"""

import pygame
import random
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
    global GRID_SIZE, grid, blocks
    GRID_SIZE = LEVEL_GRID_SIZES[level]
    grid = [[BLACK if cell == 0 else random.choice(COLORS) for cell in row] for row in LEVEL_PRE_FILLED[level]]
    blocks = LEVEL_BLOCKS[level].copy()  # Use predefined blocks for the level

# main.py
def human_mode(level):
    global selected_block, grid, blocks, score, GRID_SIZE
    running = True
    dragging = False

    # Configure the clock to control the frame rate (FPS)
    clock = pygame.time.Clock()
    FPS = 60  # Set the frame rate to 60 FPS

    while running:
        # Check if there are any valid moves left
        if no_valid_moves_left(grid, blocks, GRID_SIZE):
            print("No valid moves left! Game Over. Final Score:", score)
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH - 150 <= x <= WIDTH and 50 <= y <= (50 + len(blocks) * 100):
                    selected_index = (y - 50) // 100
                    if 0 <= selected_index < len(blocks):
                        selected_block = blocks[selected_index]
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_block:
                    x, y = pygame.mouse.get_pos()
                    snapped_position = snap_to_grid(x, y, selected_block[0], grid, GRID_SIZE, snap_range=20)
                    if snapped_position:  # Check if the adjusted position is valid
                        grid_x, grid_y = snapped_position
                        block, color = selected_block
                        if can_place_block(block, grid_x, grid_y, grid, GRID_SIZE, tolerance=2):  # Tolerance of 2 cells
                            place_block(block, grid_x, grid_y, color, grid, GRID_SIZE)
                            lines_cleared = clear_completed_lines(grid, GRID_SIZE)
                            score += lines_cleared * 10

                            # Remove the used block
                            blocks.pop(selected_index)

                            # If all blocks are used, reload all new ones
                            if not blocks:
                                blocks = LEVEL_BLOCKS[level].copy()

                            selected_block = None

                            # Check if the grid is empty (win condition)
                            if all(cell == BLACK for row in grid for cell in row):
                                print("You win! Final Score:", score)
                                running = False
                    else:
                        print("Invalid placement")
                dragging = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and selected_block:
                    block, color = selected_block
                    rotated_block = list(zip(*block[::-1]))
                    selected_block = (rotated_block, color)

        render(screen, grid, blocks, score, GRID_SIZE)
        if dragging and selected_block:
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Ensure the event queue is processed to prevent freezing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

def pc_mode(algorithm, heuristic=None, level=None):
    global grid, blocks
    state = State(grid, blocks)
    start_time = time.time()
    visited_states = 0
    max_iterations = 1000

    while not state.is_goal() and visited_states < max_iterations:
        if algorithm == "bfs":
            new_state = bfs(state, level)
        elif algorithm == "dfs":
            new_state = dfs(state, level)
        elif algorithm == "greedy":
            new_state = greedy(state, heuristic, level)
        elif algorithm == "a_star":
            new_state = a_star(state, heuristic, level)

        if new_state is None:
            print("No solution found!")
            break

        state = new_state
        grid = [row[:] for row in state.grid]
        blocks = state.blocks

        # If all blocks are used, reload all new ones
        if not blocks:
            blocks = LEVEL_BLOCKS[level].copy()

        visited_states += 1
        print(f"Visited states: {visited_states}")
        print(f"Remaining blocks: {len(state.blocks)}")
        print("Current grid:")
        for row in state.grid:
            print(row)

        render(screen, state.grid, state.blocks, score)
        pygame.time.delay(500)

    if visited_states >= max_iterations:
        print("Maximum iterations reached. No solution found.")
    else:
        print(f"Puzzle solved in {time.time() - start_time:.2f} seconds!")
        print(f"Visited states: {visited_states}")

    # Ensure the event queue is processed to prevent freezing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return


def computer_assisted_human_mode(level = None):
    """Computer-assisted human mode where the computer gives hints."""
    global grid, blocks
    state = State(grid, blocks)
    while not state.is_goal():
        # Use A* to find the next best move
        new_state = a_star(state, combined_heuristic_empty_grid, level)
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
    
    if level not in LEVEL_BLOCKS:
        print("Invalid level selected.")
        return
    
    initialize_level(level)

    if mode == "1":
        human_mode(level)
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
            pc_mode("a_star", combined_heuristic_empty_grid, level=level)
    elif mode == "3":
        computer_assisted_human_mode(level)
    pygame.quit()

if __name__ == "__main__":
    main()