from collections import deque
import heapq
from cst import *
import time

def bfs(initial_state, level):
    """
    Performs Breadth-First Search to find a solution to the wood block puzzle.
    
    BFS explores all possible states level by level, guaranteeing the shortest path solution
    if one exists. This is suitable for smaller puzzles or when optimal moves are critical.
    
    Args:
        initial_state (State): The starting configuration of the puzzle
        level (int): Current game level, used to determine valid moves
        
    Returns:
        State: The solved state if found, None otherwise
    """
    start_time = time.time()
    queue = deque([initial_state])  # Using deque for O(1) popleft operation
    visited = set()  # Track visited states using hash to prevent cycles
    
    # Using hash of state instead of full state for memory efficiency
    visited.add(hash(initial_state))

    while queue:
        # Timeout check to prevent infinite search on large puzzles
        if time.time() - start_time > 15:
            print("BFS: Time limit exceeded (15 seconds)")
            return None
            
        state = queue.popleft()
        
        # Early exit if goal is found
        if state.is_goal():
            return state

        # Generate and process successors
        for successor in state.get_successors(level):
            state_hash = hash(successor)
            if state_hash not in visited:
                visited.add(state_hash)
                queue.append(successor)

    return None

def dfs(initial_state, level):
    """
    Performs Depth-First Search to solve the puzzle.
    
    DFS explores states by going deep first, which can be memory efficient but doesn't
    guarantee optimal solutions. Useful when solution depth is unknown but may be deep.
    
    Args:
        initial_state (State): Starting puzzle configuration
        level (int): Current game level for move validation
        
    Returns:
        State: Solved state if found, None otherwise
    """
    start_time = time.time()
    stack = [initial_state]  # Using list as stack (LIFO)
    visited = set()

    while stack:
        if time.time() - start_time > 15:
            print("DFS: Time limit exceeded (15 seconds)")
            return None
            
        state = stack.pop()
        
        if state.is_goal():
            return state
            
        # Skip already visited states to prevent cycles
        if hash(state) in visited:
            continue
            
        visited.add(hash(state))
        
        # Add successors in reverse order to maintain left-to-right exploration
        stack.extend(reversed(state.get_successors(level)))

    return None

def greedy(initial_state, heuristic, level):
    """
    Performs Greedy Best-First Search using the given heuristic.
    
    Prioritizes states that appear better according to the heuristic function,
    without considering path cost. Fast but may not find optimal solutions.
    
    Args:
        initial_state (State): Starting puzzle configuration
        heuristic (function): Function that evaluates state quality
        level (int): Current game level
        
    Returns:
        State: Solved state if found, None otherwise
    """
    start_time = time.time()
    # Priority queue using only heuristic value for ordering
    heap = [(heuristic(initial_state.grid, initial_state.blocks), initial_state)]
    visited = set()

    while heap:
        if time.time() - start_time > 15:
            print("Greedy: Time limit exceeded (15 seconds)")
            return None
            
        _, state = heapq.heappop(heap)
        
        if state.is_goal():
            return state
            
        if hash(state) in visited:
            continue
            
        visited.add(hash(state))
        
        # Push successors with their heuristic evaluation
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid, successor.blocks), successor))

    return None

def a_star(initial_state, heuristic, level):
    """
    Performs A* Search combining heuristic and path cost.
    
    A* finds optimal solutions when the heuristic is admissible (never overestimates).
    Balances between Dijkstra's algorithm and Greedy search.
    
    Args:
        initial_state (State): Starting puzzle configuration
        heuristic (function): Admissible heuristic function
        level (int): Current game level
        
    Returns:
        State: Solved state if found, None otherwise
    """
    start_time = time.time()
    # Priority queue using f(n) = g(n) + h(n) where:
    # g(n) = path cost (state.moves), h(n) = heuristic value
    heap = [(heuristic(initial_state.grid, initial_state.blocks) + initial_state.moves, initial_state)]
    visited = set()

    while heap:
        if time.time() - start_time > 15:
            print("A*: Time limit exceeded (15 seconds)")
            return None
            
        _, state = heapq.heappop(heap)
        
        if state.is_goal():
            return state
            
        if hash(state) in visited:
            continue
            
        visited.add(hash(state))
        
        for successor in state.get_successors(level):
            # f(n) = actual cost so far + heuristic estimate
            total_cost = heuristic(successor.grid, successor.blocks) + successor.moves
            heapq.heappush(heap, (total_cost, successor))

    return None