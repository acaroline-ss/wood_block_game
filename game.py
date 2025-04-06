"""
State representation and generation for Wood Block Puzzle solver.

This module contains:
- The State class representing game states
- Block generation functionality
- Successor state generation logic
"""

from cst import *
from heuristics import *
import random
from utils import *


def generate_block(level):
    """
    Randomly selects a block from the available blocks for the given level.
    
    Args:
        level (int): Current game level (determines block set)
        
    Returns:
        tuple: (block_matrix, color) tuple randomly selected from LEVEL_BLOCKS[level]
        
    Example:
        >>> generate_block(1)
        ([[1, 1, 1]], (255, 0, 0))  # Could return any level 1 block
    """
    return random.choice(LEVEL_BLOCKS[level])


class State:
    """
    Represents a complete game state including:
    - Grid configuration
    - Available blocks
    - Move history
    - Search metadata
    
    Attributes:
        grid (list[list[tuple]]): 2D array of RGB colors representing current board
        blocks (list[tuple]): Available (block_matrix, color) tuples
        grid_size (int): Dimensions of the game grid (N x N)
        moves (int): Number of moves taken to reach this state
        parent (State): Previous state in solution path
        action (tuple): (block, color, x, y) of last placement
        tolerance (int): Allowed remaining colored cells for relaxed solutions
    """

    def __init__(self, grid, blocks, grid_size, moves=0, parent=None, action=None, tolerance=2):
        """
        Initialize a new game state with deep copies of mutable data.
        
        Args:
            grid: Current board state as 2D color array
            blocks: Available blocks for placement
            grid_size: Dimension of square grid
            moves: Move count (default 0)
            parent: Previous state (default None)
            action: Last move taken (default None)
            tolerance: Acceptable remaining cells (default 2)
        """
        self.grid = [row.copy() for row in grid]  # Deep copy
        self.blocks = blocks.copy()  # Deep copy
        self.grid_size = grid_size
        self.moves = moves
        self.parent = parent
        self.action = action
        self.tolerance = tolerance

    def is_goal(self):
        """
        Check if state represents a solved puzzle.
        
        Returns:
            bool: True if all grid cells are BLACK (empty)
            
        Note:
            Tolerance parameter isn't used here but may be used elsewhere
        """
        return all(cell == BLACK for row in self.grid for cell in row)

    def get_successors(self, level):
        """
        Generate all valid successor states by placing available blocks.
        
        For each block, tries:
        - All rotations
        - All valid positions
        - Handles line clearing
        - Manages block replenishment
        
        Args:
            level: Current game level for block generation
            
        Returns:
            list[State]: Valid successor states
            
        Complexity:
            O(b*r*p) where:
            b = number of blocks
            r = rotations per block (max 4)
            p = possible positions (~grid_size^2)
        """
        successors = []
        
        for i, (block, color) in enumerate(self.blocks):
            # Try all rotations
            for rotation in get_rotations(block):
                # Try all positions
                for x in range(self.grid_size):
                    for y in range(self.grid_size):
                        if can_place_block(rotation, x, y, self.grid, self.grid_size):
                            # Create new state with block placed
                            new_grid = [row.copy() for row in self.grid]
                            place_block(rotation, x, y, color, new_grid, self.grid_size)
                            clear_completed_lines(new_grid, self.grid_size)
                            
                            # Update block inventory
                            new_blocks = self.blocks.copy()
                            new_blocks.pop(i)
                            
                            # Replenish if empty
                            if not new_blocks:
                                new_blocks = LEVEL_BLOCKS[level].copy()
                            
                            successors.append(
                                State(
                                    new_grid, 
                                    new_blocks, 
                                    self.grid_size,
                                    self.moves + 1, 
                                    self, 
                                    (rotation, color, x, y),
                                    self.tolerance
                                )
                            )
        return successors

    def __hash__(self):
        """
        Generate hash for state comparison and storage.
        
        Returns:
            int: Hash based on immutable grid and sorted blocks
            
        Note:
            Sorting blocks ensures order doesn't affect equality
        """
        grid_tuple = tuple(tuple(row) for row in self.grid)
        blocks_tuple = tuple(sorted((tuple(map(tuple, b)), color) 
                         for (b, color) in self.blocks))
        return hash((grid_tuple, blocks_tuple))

    def __eq__(self, other):
        """
        Test state equality (ignores move count and parent).
        
        Args:
            other: State to compare
            
        Returns:
            bool: True if grids and blocksets match
        """
        if not isinstance(other, State):
            return False
        return (self.grid == other.grid and 
                sorted(self.blocks) == sorted(other.blocks))

    def __lt__(self, other):
        """
        Compare states for priority queue ordering.
        
        Args:
            other: State to compare
            
        Returns:
            bool: True if this state has better heuristic value
            
        Note:
            Used by A* and other informed search algorithms
        """
        return combined_heuristic(self.grid, self.blocks) < combined_heuristic(other.grid, other.blocks)