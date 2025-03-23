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
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
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
def human_mode(level):
    global selected_block, grid, blocks, score, GRID_SIZE
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
    main()  # Run the main function when the script is executed