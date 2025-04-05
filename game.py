from cst import *
from heuristics import *
import random
from utils import *


def generate_block(level):
    """
    Randomly selects a block from the available blocks for the given level.
    
    This function is used to provide new blocks when the player needs them, ensuring
    they're appropriate for the current difficulty level.
    
    Args:
        level (int): The current game level, used to determine which blocks are available.
        
    Returns:
        tuple: A randomly selected (block_matrix, color) tuple from LEVEL_BLOCKS[level].
    """
    return random.choice(LEVEL_BLOCKS[level])


class State:
    """
    Represents a game state in the wood block puzzle.
    
    A state consists of:
    - The current grid configuration
    - Available blocks
    - Move count
    - Parent state (for path tracking)
    - Action that led to this state
    - Tolerance for solution acceptance
    
    The class provides methods for:
    - Goal checking
    - Successor state generation
    - State comparison
    - Hashing for efficient storage
    """
    
    def __init__(self, grid, blocks, grid_size, moves=0, parent=None, action=None, tolerance=2):
        """
        Initialize a new game state.
        
        Args:
            grid (list[list[tuple]]): 2D array representing current grid colors
            blocks (list[tuple]): Available blocks (block_matrix, color) tuples
            grid_size (int): Size of the game grid (grid_size x grid_size)
            moves (int): Number of moves taken to reach this state
            parent (State): Previous state that led to this one
            action (tuple): (block, color, x, y) of last placement
            tolerance (int): Maximum allowed remaining colored cells to consider solution
        """
        # Deep copies to prevent accidental state modification
        self.grid = [row.copy() for row in grid]
        self.blocks = blocks.copy()
        self.grid_size = grid_size
        self.moves = moves
        self.parent = parent  # For reconstructing solution path
        self.action = action  # Track how we got here (for solution display)
        self.tolerance = tolerance  # Used for relaxed goal checking elsewhere

    def is_goal(self):
        """
        Check if this state is a winning configuration.
        
        The strict goal is achieved when the entire grid is cleared (all cells are BLACK).
        The tolerance parameter allows for relaxed checking elsewhere in the code.
        
        Returns:
            bool: True if grid is completely cleared, False otherwise
        """
        return all(cell == BLACK for row in self.grid for cell in row)

    def get_successors(self, level):
        """
        Generate all possible next states from current state.
        
        For each available block, in each possible rotation, at every valid position:
        1. Checks if placement is valid
        2. Creates new grid with block placed
        3. Clears any completed lines
        4. Creates new state with updated blocks
        
        Args:
            level (int): Current game level (used for block replenishment)
            
        Returns:
            list[State]: All valid successor states
        """
        successors = []
        
        for i, (block, color) in enumerate(self.blocks):
            # Try all rotations of current block
            for rotation in get_rotations(block):
                # Try all possible positions
                for x in range(self.grid_size):
                    for y in range(self.grid_size):
                        if can_place_block(rotation, x, y, self.grid, self.grid_size):
                            # Create new grid with block placed
                            new_grid = [row.copy() for row in self.grid]
                            place_block(rotation, x, y, color, new_grid, self.grid_size)
                            clear_completed_lines(new_grid, self.grid_size)
                            
                            # Update available blocks
                            new_blocks = self.blocks.copy()
                            new_blocks.pop(i)
                            
                            # Replenish blocks if empty (using level-appropriate set)
                            if not new_blocks:
                                new_blocks = LEVEL_BLOCKS[level].copy()
                            
                            # Record action details
                            action = (rotation, color, x, y)
                            
                            # Create new state (preserving tolerance)
                            successors.append(
                                State(new_grid, new_blocks, self.grid_size, 
                                     self.moves + 1, self, action, self.tolerance)
                            )
        return successors

    def __hash__(self):
        """
        Generate a hash for efficient state storage and comparison.
        
        Creates immutable tuples from grid and blocks to enable hashing.
        Blocks are sorted to ensure consistent hashing regardless of order.
        
        Returns:
            int: Hash value representing this state
        """
        grid_tuple = tuple(tuple(row) for row in self.grid)
        blocks_tuple = tuple(sorted((tuple(map(tuple, b)), color) 
                           for (b, color) in self.blocks))
        return hash((grid_tuple, blocks_tuple))

    def __eq__(self, other):
        """
        Check if two states are equivalent.
        
        States are equal if they have identical grids and the same blocks
        (regardless of block order).
        
        Args:
            other (State): State to compare against
            
        Returns:
            bool: True if states are equivalent
        """
        if not isinstance(other, State):
            return False
        return (self.grid == other.grid and 
                sorted(self.blocks) == sorted(other.blocks))

    def __lt__(self, other):
        """
        Compare states for priority queue ordering based on heuristic value.
        
        Used by search algorithms to prioritize promising states.
        
        Args:
            other (State): State to compare against
            
        Returns:
            bool: True if this state has lower heuristic value
        """
        return combined_heuristic(self.grid, self.blocks) < combined_heuristic(other.grid, other.blocks)