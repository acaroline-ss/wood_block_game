from collections import deque
import heapq

def bfs(initial_state):
    queue = deque([initial_state])
    while queue:
        state = queue.popleft()
        if state.is_goal():
            return state
        for successor in state.get_successors():
            queue.append(successor)
    return None

def dfs(initial_state):
    stack = [initial_state]
    while stack:
        state = stack.pop()
        if state.is_goal():
            return state
        for successor in state.get_successors():
            stack.append(successor)
    return None

def greedy(initial_state, heuristic):
    heap = [(heuristic(initial_state.grid), initial_state)]
    while heap:
        _, state = heapq.heappop(heap)
        if state.is_goal():
            return state
        for successor in state.get_successors():
            heapq.heappush(heap, (heuristic(successor.grid), successor))
    return None

def a_star(initial_state, heuristic):
    heap = [(heuristic(initial_state.grid) + initial_state.moves, initial_state)]
    while heap:
        _, state = heapq.heappop(heap)
        if state.is_goal():
            return state
        for successor in state.get_successors():
            heapq.heappush(heap, (heuristic(successor.grid) + successor.moves, successor))
    return None