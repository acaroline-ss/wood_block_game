from collections import deque
import heapq
from cst import *

MAX_DEPTH = 100  # Set a maximum depth for the search
1

def bfs(initial_state, level):
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

        if state.moves >= MAX_DEPTH:
            print("Maximum depth reached!")
            continue

        successors = state.get_successors(level)
        for successor in successors:
            queue.append(successor)

        if visited_states % 100 == 0:  # Print debug info less frequently
            print(f"Visited states: {visited_states}")
            print(f"Remaining blocks: {len(state.blocks)}")
            print("Current grid:")
            for row in state.grid:
                print(row)

    print("No solution found!")
    return None

def dfs(initial_state, level):
    stack = [initial_state]
    visited = set()

    while stack:
        state = stack.pop()
        if state.is_goal():
            return state

        if hash(state) in visited:
            continue

        visited.add(hash(state))
        for successor in state.get_successors(level):
            stack.append(successor)

    return None

def greedy(initial_state, heuristic, level):
    heap = [(heuristic(initial_state.grid), initial_state)]
    visited = set()

    while heap:
        _, state = heapq.heappop(heap)
        if state.is_goal():
            return state

        if hash(state) in visited:
            continue

        visited.add(hash(state))
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid), successor))

    return None

def a_star(initial_state, heuristic, level):
    heap = [(heuristic(initial_state.grid) + initial_state.moves, initial_state)]
    visited = set()

    while heap:
        _, state = heapq.heappop(heap)
        if state.is_goal():
            return state

        if hash(state) in visited:
            continue

        visited.add(hash(state))
        for successor in state.get_successors(level):
            heapq.heappush(heap, (heuristic(successor.grid) + successor.moves, successor))

    return None