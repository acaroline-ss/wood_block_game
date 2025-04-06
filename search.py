from collections import deque
import heapq
from cst import *
import time

def bfs(initial_state, level):
    """
    Performs Breadth-First Search to find the optimal solution to the wood block puzzle.
    
    Args:
        initial_state (State): The starting configuration of the puzzle
        level (int): Current game level, used to determine valid moves
        
    Returns:
        State: The solved state if found within time limit, None otherwise
        
    Notes:
        - Explores all possible states level by level
        - Guarantees shortest path solution (optimal moves)
        - Uses deque for O(1) popleft operations
        - Tracks visited states using hash for memory efficiency
        - Implements 15-second timeout for large puzzles
    """
    start_time = time.time()
    queue = deque([initial_state])
    visited = {hash(initial_state)}

    while queue:
        if time.time() - start_time > 15:
            print("BFS: Time limit exceeded (15 seconds)")
            return None
            
        state = queue.popleft()
        
        if state.is_goal():
            return state

        for successor in state.get_successors(level):
            if (h := hash(successor)) not in visited:
                visited.add(h)
                queue.append(successor)

    return None

def dfs(initial_state, level):
    """
    Performs Depth-First Search to solve the puzzle (non-optimal solution).
    
    Args:
        initial_state (State): Starting puzzle configuration
        level (int): Current game level for move validation
        
    Returns:
        State: Solved state if found within time limit, None otherwise
        
    Notes:
        - Explores by going deep first (memory efficient for deep solutions)
        - Doesn't guarantee optimal solutions
        - Processes successors in reverse order to maintain left-to-right exploration
        - Implements cycle detection via visited set
    """
    start_time = time.time()
    stack = [initial_state]
    visited = set()

    while stack:
        if time.time() - start_time > 15:
            print("DFS: Time limit exceeded (15 seconds)")
            return None
            
        state = stack.pop()
        
        if state.is_goal():
            return state
            
        if (h := hash(state)) in visited:
            continue
            
        visited.add(h)
        stack.extend(reversed(state.get_successors(level)))

    return None

def greedy(initial_state, heuristic, level):
    """
    Greedy Best-First Search using heuristic evaluation.
    
    Args:
        initial_state (State): Starting puzzle configuration
        heuristic (function): Function that evaluates state quality (h(n))
        level (int): Current game level
        
    Returns:
        State: Solved state if found within time limit, None otherwise
        
    Notes:
        - Prioritizes states with best heuristic value
        - No consideration of path cost (g(n))
        - May find solutions quickly but not necessarily optimal
        - Uses priority queue (min-heap) for state selection
    """
    start_time = time.time()
    heap = [(heuristic(initial_state.grid, initial_state.blocks), initial_state)]
    visited = set()

    while heap:
        if time.time() - start_time > 15:
            print("Greedy: Time limit exceeded (15 seconds)")
            return None
            
        _, state = heapq.heappop(heap)
        
        if state.is_goal():
            return state
            
        if (h := hash(state)) in visited:
            continue
            
        visited.add(h)
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid, successor.blocks), successor))

    return None

def a_star(initial_state, heuristic, level):
    """
    A* Search combining path cost and heuristic (f(n) = g(n) + h(n)).
    
    Args:
        initial_state (State): Starting puzzle configuration
        heuristic (function): Admissible heuristic function (never overestimates)
        level (int): Current game level
        
    Returns:
        State: Solved state if found within time limit, None otherwise
        
    Notes:
        - Finds optimal solutions when heuristic is admissible
        - Balances between path cost and heuristic estimate
        - More efficient than BFS for large state spaces with good heuristic
    """
    start_time = time.time()
    heap = [(heuristic(initial_state.grid, initial_state.blocks) + initial_state.moves, initial_state)]
    visited = set()

    while heap:
        if time.time() - start_time > 15:
            print("A*: Time limit exceeded (15 seconds)")
            return None
            
        _, state = heapq.heappop(heap)
        
        if state.is_goal():
            return state
            
        if (h := hash(state)) in visited:
            continue
            
        visited.add(h)
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid, successor.blocks) + successor.moves, successor))

    return None