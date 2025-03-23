from collections import deque 
import heapq  
from cst import * 

"""
    Performs Breadth-First Search to find a solution to the puzzle.
    
    Args:
        initial_state (State): The starting state of the puzzle.
        level (int): The current level of the game.
    
    Returns:
        State: The goal state if found, otherwise None.
    """
def bfs(initial_state, level):
    queue = deque([initial_state])  # Initialize a queue with the initial state
    visited = set()  # Track visited states to avoid revisiting
    visited.add(hash(initial_state))  # Add the initial state to the visited set

    while queue:  # Continue until the queue is empty
        state = queue.popleft()  # Get the next state from the queue
        if state.is_goal():  # Check if the current state is the goal
            print("Goal state found!")
            return state  # Return the goal state

        # Generate all possible successor states
        successors = state.get_successors(level)
        for successor in successors:
            state_hash = hash(successor)  # Compute the hash of the successor state
            if state_hash not in visited:  # If the state hasn't been visited
                visited.add(state_hash)  # Mark it as visited
                queue.append(successor)  # Add it to the queue
                print(f"Generated successor: {successor.grid}")  # Print the successor grid

    print("No solution found!")  # If no solution is found
    return None  # Return None

"""
    Performs Depth-First Search to find a solution to the puzzle.
    
    Args:
        initial_state (State): The starting state of the puzzle.
        level (int): The current level of the game.
    
    Returns:
        State: The goal state if found, otherwise None.
    """
def dfs(initial_state, level):
    stack = [initial_state]  # Initialize a stack with the initial state
    visited = set()  # Track visited states to avoid revisiting

    while stack:  # Continue until the stack is empty
        state = stack.pop()  # Get the next state from the stack
        if state.is_goal():  # Check if the current state is the goal
            return state  # Return the goal state

        if hash(state) in visited:  # If the state has already been visited
            continue  # Skip it

        visited.add(hash(state))  # Mark the state as visited
        # Generate all possible successor states and add them to the stack
        for successor in state.get_successors(level):
            stack.append(successor)

    return None  # If no solution is found, return None

"""
    Performs Greedy Search to find a solution to the puzzle.
    Uses a heuristic function to prioritize states.
    
    Args:
        initial_state (State): The starting state of the puzzle.
        heuristic (function): A heuristic function to evaluate states.
        level (int): The current level of the game.
    
    Returns:
        State: The goal state if found, otherwise None.
    """
def greedy(initial_state, heuristic, level):
    heap = [(heuristic(initial_state.grid), initial_state)]  # Initialize a priority queue with the initial state
    visited = set()  # Track visited states to avoid revisiting

    while heap:  # Continue until the priority queue is empty
        _, state = heapq.heappop(heap)  # Get the state with the lowest heuristic value
        if state.is_goal():  # Check if the current state is the goal
            return state  # Return the goal state

        if hash(state) in visited:  # If the state has already been visited
            continue  # Skip it

        visited.add(hash(state))  # Mark the state as visited
        # Generate all possible successor states and add them to the priority queue
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid), successor))

    return None  # If no solution is found, return None

"""
    Performs A* Search to find a solution to the puzzle.
    Uses a heuristic function combined with the cost to prioritize states.
    
    Args:
        initial_state (State): The starting state of the puzzle.
        heuristic (function): A heuristic function to evaluate states.
        level (int): The current level of the game.
    
    Returns:
        State: The goal state if found, otherwise None.
    """
def a_star(initial_state, heuristic, level):
    heap = [(heuristic(initial_state.grid) + initial_state.moves, initial_state)]  # Initialize a priority queue with the initial state
    visited = set()  # Track visited states to avoid revisiting

    while heap:  # Continue until the priority queue is empty
        _, state = heapq.heappop(heap)  # Get the state with the lowest combined heuristic + cost value
        if state.is_goal():  # Check if the current state is the goal
            return state  # Return the goal state

        if hash(state) in visited:  # If the state has already been visited
            continue  # Skip it

        visited.add(hash(state))  # Mark the state as visited
        # Generate all possible successor states and add them to the priority queue
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid) + successor.moves, successor))

    return None  # If no solution is found, return None