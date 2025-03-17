from collections import deque
import heapq


MAX_DEPTH = 100  # Set a maximum depth for the search

def bfs(initial_state):
    queue = deque([initial_state])  # Fila para armazenar os estados a serem explorados
    visited = set()  # Conjunto para armazenar estados já visitados
    visited_states = 0  # Contador de estados visitados

    while queue:  # Enquanto houver estados na fila
        state = queue.popleft()  # Remove o primeiro estado da fila
        if state.is_goal():  # Verifica se o estado atual é o objetivo
            print("Goal state found!")
            return state  # Retorna o estado objetivo

        if hash(state) in visited:  # Se o estado já foi visitado, pula para o próximo
            continue

        visited.add(hash(state))  # Marca o estado como visitado
        visited_states += 1  # Incrementa o contador de estados visitados

        for row in state.grid:  # Exibe a grade atual no console (para depuração)
            print(row)

        if state.moves >= MAX_DEPTH:  # Verifica se o limite de profundidade foi atingido - para evitar loops infinitos !
            print("Maximum depth reached!")
            continue  # Pula para o próximo estado

        successors = state.get_successors()  # Gera os sucessores do estado atual
        for successor in successors:  # Adiciona os sucessores à fila
            queue.append(successor)

        print(f"Visited states: {visited_states}")  # Exibe o número de estados visitados
        print(f"Remaining blocks: {len(state.blocks)}")  # Exibe o número de blocos restantes
        print("Current grid:")  # Exibe a grade atual

    print("No solution found!")  # Se a fila estiver vazia e nenhum objetivo foi encontrado
    return None

def dfs(initial_state):
    stack = [initial_state]  # Pilha para armazenar os estados a serem explorados
    visited = set()  # Conjunto para armazenar estados já visitados

    while stack:  # Enquanto houver estados na pilha
        state = stack.pop()  # Remove o último estado da pilha
        if state.is_goal():  # Verifica se o estado atual é o objetivo
            return state  # Retorna o estado objetivo

        if hash(state) in visited:  # Se o estado já foi visitado, pula para o próximo
            continue

        visited.add(hash(state))  # Marca o estado como visitado
        for successor in state.get_successors():  # Gera e adiciona os sucessores à pilha
            stack.append(successor)

    return None  # Se a pilha estiver vazia e nenhum objetivo foi encontrado

def greedy(initial_state, heuristic):
    heap = [(heuristic(initial_state.grid, initial_state.blocks), initial_state)]  # Heap com (heurística, estado)
    visited = set()  # Conjunto para armazenar estados já visitados

    while heap:  # Enquanto houver estados no heap
        _, state = heapq.heappop(heap)  # Remove o estado com menor valor de heurística
        if state.is_goal():  # Verifica se o estado atual é o objetivo
            return state  # Retorna o estado objetivo

        if hash(state) in visited:  # Se o estado já foi visitado, pula para o próximo
            continue

        visited.add(hash(state))  # Marca o estado como visitado
        for successor in state.get_successors():  # Gera e adiciona os sucessores ao heap
            heapq.heappush(heap, (heuristic(successor.grid, successor.blocks), successor))

    return None  # Se o heap estiver vazia e nenhum objetivo foi encontrado

def a_star(initial_state, heuristic):
    heap = [(heuristic(initial_state.grid, initial_state.blocks) + initial_state.moves, initial_state)]  # Heap com (heurística + custo, estado)
    visited = set()  # Conjunto para armazenar estados já visitados

    while heap:  # Enquanto houver estados no heap
        _, state = heapq.heappop(heap)  # Remove o estado com menor valor de heurística + custo
        if state.is_goal():  # Verifica se o estado atual é o objetivo
            return state  # Retorna o estado objetivo

        if hash(state) in visited:  # Se o estado já foi visitado, pula para o próximo
            continue

        visited.add(hash(state))  # Marca o estado como visitado
        for successor in state.get_successors():  # Gera e adiciona os sucessores ao heap
            heapq.heappush(heap, (heuristic(successor.grid, successor.blocks) + successor.moves, successor))

    return None  # Se o heap estiver vazia e nenhum objetivo foi encontrado


