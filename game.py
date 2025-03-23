from cst import *
from heuristics import *
import random
from utils import *

"""
    Generates a random block from the list of blocks available for the given level.
    
    Args:
        level (int): The current level of the game.
    
    Returns:
        list: A randomly selected block from the LEVEL_BLOCKS list for the given level.
"""
def generate_block(level):
    return random.choice(LEVEL_BLOCKS[level])


"""
    The State class represents the current state of the game, including the grid, blocks, and moves.
    It also provides methods to generate successor states and check if the goal state is reached.
"""

class State:

    """
        Initializes a new State object.
        
        Args:
            grid (list): A 2D list representing the current state of the grid.
            blocks (list): A list of tuples representing the blocks and their colors.
            moves (int): The number of moves taken to reach this state (default is 0).
            parent (State): The parent state from which this state was derived (default is None).
    """
    def __init__(self, grid, blocks, moves=0, parent=None):
        self.grid = [row.copy() for row in grid] # Create a copy of the grid to avoid modifying the original
        self.blocks = blocks.copy() # Create a copy of the blocks list
        self.moves = moves # Number of moves taken to reach this state
        self.parent = parent   # Reference to the parent state (used to track the path)

    """
        Checks if the current state is the goal state.
        
        Returns:
            bool: True if all cells in the grid are BLACK, indicating the goal state.
    """
    def is_goal(self):
        return all(cell == BLACK for row in self.grid for cell in row)

    """
        Generates all possible successor states from the current state.
        
        Args:
            level (int): The current level of the game.
        
        Returns:
            list: A list of State objects representing all possible successor states.
    """
    def get_successors(self, level):
        successors = [] # Initialize an empty list to store successor states

        for block, color in self.blocks:  # Iterate over each block and its color in the current state

            for rotation in get_rotations(block): # Get all possible rotations of the current block

                block_height = len(rotation)  # Height of the rotated block
                block_width = len(rotation[0]) if block_height > 0 else 0  # Height of the rotated block

                 # Calculate the maximum x and y positions where the block can be placed
                max_x = GRID_SIZE - block_width 
                max_y = GRID_SIZE - block_height
            
                # Iterate over all possible positions (x, y) where the block can be placed
                for x in range(max_x + 1):
                    for y in range(max_y + 1):
                        # Check if the block can be placed at the current position
                        if can_place_block(rotation, x, y, self.grid, GRID_SIZE):
                            new_grid = [row.copy() for row in self.grid] # Create a copy of the current grid to avoid modifying it
                            place_block(rotation, x, y, color, new_grid, GRID_SIZE) # Place the block on the new grid at the specified position
                            clear_completed_lines(new_grid, GRID_SIZE)  # Clear any completed lines on the new grid
                            new_blocks = [b for b in self.blocks if b != (block, color)] # Create a new list of blocks, removing the block that was just placed
                            successors.append(State(new_grid, new_blocks, self.moves + 1, self)) # Create a new State object representing the successor state
                            print(f"Generated successor at ({x}, {y}) with block {block}") #debbug
        return successors

    """
        Generates a hash value for the State object.
        
        Returns:
            int: A hash value based on the grid and blocks.
    """
    def __hash__(self):
        grid_tuple = tuple(tuple(row) for row in self.grid) # Convert the grid to a tuple of tuples
        blocks_tuple = tuple(sorted((tuple(map(tuple, b)), color) for (b, color) in self.blocks)) # Convert blocks to a sorted tuple
        return hash((grid_tuple, blocks_tuple))  # Return the hash of the combined tuple

    """
        Checks if two State objects are equal.
        
        Args:
            other (State): Another State object to compare with.
        
        Returns:
            bool: True if the grid and blocks of both states are equal.
    """
    def __eq__(self, other):
        return (self.grid == other.grid and 
                sorted(self.blocks) == sorted(other.blocks))

    """
        Compares two State objects based on their heuristic values.
        
        Args:
            other (State): Another State object to compare with.
        
        Returns:
            bool: True if the heuristic value of this state is less than the other state.
    """
    def __lt__(self, other):
        return combined_heuristic(self.grid, self.blocks) < combined_heuristic(other.grid, other.blocks)