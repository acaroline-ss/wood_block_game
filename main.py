import pygame
import render
import random
from collections import deque
import heapq
import time



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

#sizes
WIDTH = 800
HEIGHT = 600

# Block shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1], [1, 1]],         # Square
    [[1, 1, 1, 1]],            # Line
    [[1, 1, 0], [0, 1, 1]],    # Z-shape
    [[0, 1, 1], [1, 1, 0]],    # S-shape
    [[1, 0], [1, 0], [1, 1]],  # L-shape
    [[0, 1], [0, 1], [1, 1]],  # Reverse L-shape
    [[1]], # single square
    [[1,1]], #small rectangle
    [[1,1,1]], # medium rectangle/line
    [[1,1,1],[1,1,1],[1,1,1]], # big square
    [[1,1],[0,1]], #small corner
    [[1,1,1],[0,0,1],[0,0,1]], #big corner
]

# Grid settings
GRID_SIZE = int(input("Enter grid size (e.g., 5, 6, 7): "))
grid = [[BLACK for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
BLOCK_SIZE = 40









# Generate a random block
def generate_block():
    return random.choice(SHAPES), random.choice(COLORS)

# State representation
class State:
    def __init__(self, grid, blocks, moves=0):
        self.grid = grid
        self.blocks = blocks
        self.moves = moves

    def is_goal(self):
        return all(cell == BLACK for row in self.grid for cell in row)

    def get_successors(self):
        print("get_successors called!")  # Debugging
        successors = []
        if not self.blocks:
            print("No blocks left!")
            return successors
        block, color = self.blocks[0]  # Only consider the first block
        for rotation in get_rotations(block):
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, self.grid):
                        new_grid = [row[:] for row in self.grid]
                        place_block(rotation, x, y, color, new_grid)
                        new_blocks = self.blocks[1:]  # Remove the placed block
                        new_blocks.append(generate_block())  # Add a new block to replace the consumed one
                        successors.append(State(new_grid, new_blocks, self.moves + 1))
        return successors


    def __hash__(self):
        grid_tuple = tuple(map(tuple, self.grid))  # Convert grid to a tuple of tuples
        blocks_tuple = tuple((tuple(map(tuple, block)), color) for block, color in self.blocks)  # Convert blocks to a tuple of tuples
        return hash((grid_tuple, blocks_tuple))  # Hash the combined tuple

    def __eq__(self, other):
        return self.grid == other.grid and self.blocks == other.blocks


    def __lt__(self, other):
        return heuristic_empty_cells(self.grid) < heuristic_empty_cells(other.grid)
    


# Helper functions
def get_rotations(block):
    rotations = [block]
    for _ in range(3):
        block = [list(row) for row in zip(*block[::-1])]  # Rotate 90 degrees
        rotations.append(block)
    return rotations

def can_place_block(block, x, y, grid):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                if (x + col < 0 or x + col >= GRID_SIZE or
                    y + row < 0 or y + row >= GRID_SIZE or
                    grid[y + row][x + col] != BLACK):
                    return False
    return True

def place_block(block, x, y, color, grid):
    for row in range(len(block)):
        for col in range(len(block[row])):
            if block[row][col]:
                grid[y + row][x + col] = color
                print(f"Placed block at ({x + col}, {y + row})")  # Debugging

def no_valid_moves_left(grid, blocks):
    for block, color in blocks:
        for rotation in get_rotations(block):
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid):
                        return False
    return True

def clear_completed_lines(grid):
    """
    Clears completed rows and columns and returns the number of lines cleared.
    """
    lines_cleared = 0

    # Check for completed rows
    rows_to_clear = []
    for y in range(GRID_SIZE):
        if all(cell != BLACK for cell in grid[y]):
            rows_to_clear.append(y)

    # Check for completed columns
    cols_to_clear = []
    for x in range(GRID_SIZE):
        if all(grid[y][x] != BLACK for y in range(GRID_SIZE)):
            cols_to_clear.append(x)

    # Clear completed rows
    for y in rows_to_clear:
        for x in range(GRID_SIZE):
            grid[y][x] = BLACK
        lines_cleared += 1

    # Clear completed columns
    for x in cols_to_clear:
        for y in range(GRID_SIZE):
            grid[y][x] = BLACK
        lines_cleared += 1

    return lines_cleared


def place_random_block(grid, blocks):
    if not blocks:
        return grid, blocks

    for _ in range(len(blocks)):  # Try all blocks
        block, color = random.choice(blocks)
        rotations = get_rotations(block)
        for rotation in rotations:
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid):
                        place_block(rotation, x, y, color, grid)
                        blocks.remove((block, color))
                        return grid, blocks
    print("No valid placement found for any block!")
    return grid, blocks





def heuristic_empty_cells(grid):
    return sum(cell == BLACK for row in grid for cell in row)

def heuristic_row_completion(grid):
    completed_rows = sum(all(cell != BLACK for cell in row) for row in grid)
    return -completed_rows

def combined_heuristic(grid):
    empty_cells = sum(cell == BLACK for row in grid for cell in row)
    completed_rows = sum(all(cell != BLACK for cell in row) for row in grid)
    completed_cols = sum(all(grid[y][x] != BLACK for y in range(GRID_SIZE)) for x in range(GRID_SIZE))
    return empty_cells - (completed_rows + completed_cols)  # Minimize empty cells and maximize completed lines

def block_count_heuristic(grid, blocks):
    """
    Heuristic that prioritizes minimizing the number of remaining blocks.
    """
    return len(blocks)  # Fewer remaining blocks are better









def draw_grid(screen, grid):
    """
    Draw the grid on the screen.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_blocks(screen, blocks):
    """
    Draw the available blocks on the screen.
    """
    for i, (block, color) in enumerate(blocks):
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    pygame.draw.rect(screen, color, (WIDTH - 150 + col * BLOCK_SIZE, 50 + row * BLOCK_SIZE + i * 100, BLOCK_SIZE, BLOCK_SIZE))

def render(screen, grid, blocks, score):
    """
    Render the entire game state (grid, blocks, and score).
    """
    screen.fill(WHITE)
    draw_grid(screen, grid)
    draw_blocks(screen, blocks)
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))
    pygame.display.flip()










MAX_DEPTH = 100  # Set a maximum depth for the search

def bfs(initial_state):
    queue = deque([initial_state])
    visited = set()
    visited_states = 0
    while queue:
        state = queue.popleft()
        if state.is_goal():
            print("Goal state found!")
            return state
        if hash(state) in visited:
            continue
        visited.add(hash(state))
        visited_states += 1
        for row in state.grid:
            print(row)
        if state.moves >= MAX_DEPTH:  # Stop if the maximum depth is reached
            print("Maximum depth reached!")
            continue
        successors = state.get_successors()
        for successor in successors:
            queue.append(successor)
        print(f"Visited states: {visited_states}")
        print(f"Remaining blocks: {len(state.blocks)}")
        print("Current grid:")
    print("No solution found!")
    return None

def dfs(initial_state):
    stack = [initial_state]
    visited = set()
    while stack:
        state = stack.pop()
        if state.is_goal():
            return state
        if hash(state) in visited:
            continue
        visited.add(hash(state))
        for successor in state.get_successors():
            stack.append(successor)
    return None

def greedy(initial_state, heuristic):
    heap = [(heuristic(initial_state.grid, blocks), initial_state)]
    visited = set()
    while heap:
        _, state = heapq.heappop(heap)
        if state.is_goal():
            return state
        if hash(state) in visited:
            continue
        visited.add(hash(state))
        for successor in state.get_successors():
            heapq.heappush(heap, (heuristic(successor.grid, blocks), successor))
    return None

def a_star(initial_state, heuristic):
    heap = [(heuristic(initial_state.grid, blocks) + initial_state.moves, initial_state)]
    visited = set()
    while heap:
        _, state = heapq.heappop(heap)
        if state.is_goal():
            return state
        if hash(state) in visited:
            continue
        visited.add(hash(state))
        for successor in state.get_successors():
            heapq.heappush(heap, (heuristic(successor.grid, blocks) + successor.moves, successor))
    return None











# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wood Block Puzzle")

# Game setup
grid = [[BLACK for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
blocks = [generate_block() for _ in range(3)]
selected_block = None
score = 0





# Game modes
def pc_mode(algorithm, heuristic=None):
    global grid, blocks
    # Place a random block to ensure the board is not empty
    grid, blocks = place_random_block(grid, blocks)
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
        
        # Update the state, grid, and blocks
        state = new_state
        grid = [row[:] for row in state.grid]  # Update the grid
        blocks = state.blocks  # Update the blocks

        #if len(state.blocks) < 3 :
        #    state.blocks.append(generate_block())
        #    print("hihi")

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


def human_mode():
    global selected_block, grid, blocks, score
    running = True
    dragging = False
    drag_pos = (0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if WIDTH - 150 <= x <= WIDTH - 50 and 50 <= y <= 350:
                    selected_index = (y - 50) // 100
                    selected_block = blocks[selected_index]
                    dragging = True
                    drag_pos = (x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and selected_block:
                    grid_x, grid_y = drag_pos[0] // BLOCK_SIZE, drag_pos[1] // BLOCK_SIZE
                    block, color = selected_block
                    if can_place_block(block, grid_x, grid_y, grid):
                        place_block(block, grid_x, grid_y, color, grid)
                        # Clear completed lines and update score
                        lines_cleared = clear_completed_lines(grid)
                        score += lines_cleared * 10  # Bonus points for cleared lines
                        # Replace the placed block with a new one
                        blocks[selected_index] = generate_block()
                        selected_block = None
                        # Check if the grid is fully cleared
                        if all(cell != BLACK for row in grid for cell in row):
                            print("You win! Final Score:", score)
                            running = False
                        score += 10
                        if all(cell == BLACK for row in grid for cell in row):
                            print("You win! Final Score:", score)
                            running = False
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                drag_pos = pygame.mouse.get_pos()
            elif event.type == pygame.KEYDOWN:  # Add key press event handling
                if event.key == pygame.K_SPACE:  # Rotate block on spacebar press
                    if selected_block:
                        block, color = selected_block
                        rotated_block = list(zip(*block[::-1]))  # Rotate 90 degrees clockwise
                        selected_block = (rotated_block, color)
        if no_valid_moves_left(grid, blocks):
            print("No valid moves left! Game Over. Final Score:", score)
            running = False
        render(screen, grid, blocks, score)
        if dragging and selected_block:
            block, color = selected_block
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (drag_pos[0] + col * BLOCK_SIZE, drag_pos[1] + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()




        

# Main function
def main():
    global GRID_SIZE, grid, blocks
    print("Welcome to Wood Block Puzzle!")
    print("1. PC Mode")
    print("2. Human Mode")
    mode = input("Select mode (1/2): ")
    if mode == "1":
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
            pc_mode("greedy", block_count_heuristic)
        elif algorithm == "4":
            pc_mode("a_star", block_count_heuristic)
    elif mode == "2":
        human_mode()
    pygame.quit()

if __name__ == "__main__":
    main()