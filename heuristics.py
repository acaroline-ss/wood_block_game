"""
Heuristic evaluation functions for Wood Block Puzzle solver.

This module provides various heuristic functions to evaluate game states,
used by search algorithms to estimate state quality without full exploration.
"""

from cst import *
from utils import *

def heuristic_filled_cells(grid, blocks=None):
    """
    Counts the number of non-empty (filled) cells in the grid.
    
    This is the simplest possible heuristic - lower values indicate better states
    (closer to solution). Works well for greedy search but lacks strategic insight.

    Args:
        grid: 2D array of RGB tuples representing current board state
        blocks: Ignored (present for interface consistency)

    Returns:
        int: Number of non-BLACK cells (0 is perfect score)

    Example:
        >>> grid = [[BLACK, WHITE], [WHITE, BLACK]]
        >>> heuristic_filled_cells(grid)
        2
    """
    return sum(cell != BLACK for row in grid for cell in row)

def heuristic_remaining_blocks(grid, blocks):
    """
    Evaluates state based on number of unplaced blocks.
    
    Fewer remaining blocks generally indicates progress toward solution.
    However, this alone doesn't account for board configuration.

    Args:
        grid: Ignored (present for interface consistency)
        blocks: List of (block_matrix, color) tuples remaining

    Returns:
        int: Count of remaining blocks (0 is perfect score)

    Note:
        Works best when combined with other heuristics
    """
    return len(blocks)

def combined_heuristic(grid, blocks):
    """
    Comprehensive state evaluation combining multiple strategic factors.
    
    Components:
    1. Filled cells penalty (more = worse)
    2. Potential line clear bonus (more = better)
    3. Block options bonus (more = better)
    
    Weights were determined empirically through testing.

    Args:
        grid: Current board state
        blocks: Remaining blocks

    Returns:
        int: Weighted heuristic score (lower is better)

    Note:
        The weights (10 for lines, 5 for blocks) can be tuned for
        different game levels or difficulty settings.
    """
    grid_size = len(grid)
    
    # Filled cells (direct measure of progress)
    filled = sum(cell != BLACK for row in grid for cell in row)
    
    # Potential line clears (strategic bonus)
    lines = 0
    lines += sum(all(cell != BLACK for cell in row) for row in grid)
    lines += sum(all(grid[i][j] != BLACK for i in range(grid_size))
                for j in range(grid_size))
    
    return (
        filled          # Base penalty
        - lines * 10    # Strong bonus for clearable lines
        + len(blocks) * 5  # Moderate bonus for having options
    )

def heuristic_block_removal(grid, blocks):
    """
    Estimates how many remaining blocks can potentially be placed.
    
    This evaluates flexibility - states where more blocks can be placed
    are considered better, as they provide more solution paths.

    Args:
        grid: Current board state
        blocks: Remaining (block_matrix, color) tuples

    Returns:
        int: Negative count of placeable blocks (lower is better)

    Complexity:
        O(b*r*p) where:
        b = number of blocks
        r = rotations per block (max 4)
        p = grid positions (N^2)
    """
    removable_blocks = 0
    grid_size = len(grid)
    
    for block, _ in blocks:  # Color not needed for placement check
        # Check all rotations
        for rotation in get_rotations(block):
            # Check all positions - using any() for early termination
            if any(can_place_block(rotation, x, y, grid)
                  for x in range(grid_size)
                  for y in range(grid_size)):
                removable_blocks += 1
                break  # Found at least one placement
            
    return -removable_blocks  # Negative because fewer is better