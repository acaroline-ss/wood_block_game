import pygame
import render
import random
from collections import deque
import heapq
import time



# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)] #red, green, blue, yellow, purple

#sizes
WIDTH = 800 #TODO WHAT IS THIS FOR
HEIGHT = 600 #TODO ?

# Block shapes
SHAPES = [
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1], [1, 1]],         # Square
    [[1, 1, 1, 1]],            # Line
    [[1, 1, 0], [0, 1, 1]],    # Z-shape
    [[0, 1, 1], [1, 1, 0]],    # S-shape
    [[1, 0], [1, 0], [1, 1]],  # L-shape
    [[0, 1], [0, 1], [1, 1]],  # Reverse L-shape
    [[1]], # single square
    [[1,1]], #small rectangle
    [[1,1,1]], # medium rectangle/line
    [[1,1,1],[1,1,1],[1,1,1]], # big square
    [[1,1],[0,1]], #small corner
    [[1,1,1],[0,0,1],[0,0,1]], #big corner
]

# Grid settings
GRID_SIZE = int(input("Enter grid size (e.g., 5, 6, 7): ")) #Pede input ao jogador para poder variar o size do grid
grid = [[BLACK for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] #cria um grid preto de tamanho que foi input
BLOCK_SIZE = 40 #TODO wtf









# Generate a random block
def generate_block():
    return random.choice(SHAPES), random.choice(COLORS) 

# State representation
class State:
    #estado initial - "construtor de classes" (prgramação orientado objeto)
    def __init__(self, grid, blocks, moves=0): #self = instancia da class
        self.grid = grid #faz com que as instancias possam ser accessed and modified
        self.blocks = blocks
        self.moves = moves

    #define qual é o objetivo do jogo (aka estado final)
    def is_goal(self):
        return all(cell == BLACK for row in self.grid for cell in row)
    
    #define os próximos estados possiveis consuante o estado corrente
    def get_successors(self):
        print("get_successors called!")  # Debugging
        successors = []
        if not self.blocks:
            print("No blocks left!") # não suposto tho - mais para debugging porque se forem sempre replaced = infinite
            return successors
        block, color = self.blocks[0]  #vai buscar o primeiro bloco e a sua cor do self.block
        for rotation in get_rotations(block): #itera sobre todas as diferentes orientações possiveis 
            for x in range(GRID_SIZE):  
                for y in range(GRID_SIZE): #itera sobre todas as posições possiveis
                    if can_place_block(rotation, x, y, self.grid): #verifica para cada rotação e posição se o bloco pode ser colocado
                        new_grid = [row[:] for row in self.grid] #se pode ser colocado, cria new grid (cópia da self.grid = current grid)
                        place_block(rotation, x, y, color, new_grid) #o bloco é colocado
                        new_blocks = self.blocks[1:]  # tira the placed block dos blocos a colocar ("to be placed")
                        new_blocks.append(generate_block())  # Add a new block to replace the consumed one 
                        successors.append(State(new_grid, new_blocks, self.moves + 1)) # Um novo estado é criado com a updated grid, blocks, e mais um move
        return successors

    #permite que instâncias da classe sejam usadas como chaves em dicionários ou armazenadas em conjuntos - garante a imutabilidade
    def __hash__(self):
        grid_tuple = tuple(map(tuple, self.grid))  # Convert grid to a tuple of tuples
        blocks_tuple = tuple((tuple(map(tuple, block)), color) for block, color in self.blocks)  # Convert blocks to a tuple of tuples
        return hash((grid_tuple, blocks_tuple))  # Hash the combined tuple

    #verifica se dois objetos são iguais
    def __eq__(self, other):
        return self.grid == other.grid and self.blocks == other.blocks

    #verifica se um é menor que o outro (neste caso especificamente para as heuristics)
    def __lt__(self, other):
        return heuristic_empty_cells(self.grid) < heuristic_empty_cells(other.grid)
    


# Helper functions
def get_rotations(block):
    rotations = [block] # a lista das rotações é initializada com o bloco na sua rotação original (0º)
    for _ in range(3): #três vezes para as três rotações
        block = [list(row) for row in zip(*block[::-1])]  #block[::-1]: Inverte a ordem das linhas do bloco (rotação inicial). zip(*block[::-1]): Transpõe o bloco (troca linhas por colunas).[list(row) for row in ...]: Converte o resultado de volta em uma lista de listas (matriz).
        rotations.append(block) # adiciona a rotação a lista
    return rotations

def can_place_block(block, x, y, grid):
    for row in range(len(block)):
        for col in range(len(block[row])): #percore cada "célula" do bloco
            if block[row][col]: 
                if (x + col < 0 or x + col >= GRID_SIZE or 
                    y + row < 0 or y + row >= GRID_SIZE or
                    grid[y + row][x + col] != BLACK): #verifica se a posição correspondente na grid está na grid (depasse pas) ou se não está occupada
                    return False
    return True

def place_block(block, x, y, color, grid):
    for row in range(len(block)):
        for col in range(len(block[row])):#percore cada "célula" do bloco
            if block[row][col]:
                grid[y + row][x + col] = color #Atualiza a célula correspondente na grid com a cor especificada
                print(f"Placed block at ({x + col}, {y + row})")  # Debugging

def no_valid_moves_left(grid, blocks):
    for block, color in blocks: #percore lista de blocso
        for rotation in get_rotations(block): #percore lista de rotações
            for x in range(GRID_SIZE): 
                for y in range(GRID_SIZE): #percore a grid
                    if can_place_block(rotation, x, y, grid): 
                        return False 
    return True #só return true se nenhum dos blocos em nenhumas das rotações pode ser placed

def clear_completed_lines(grid):
    #Clears completed rows and columns and returns the number of lines cleared.
    lines_cleared = 0

    # Check for completed rows
    rows_to_clear = []
    for y in range(GRID_SIZE):
        if all(cell != BLACK for cell in grid[y]): #se toda a coluna estiver cheia (aka colorida)
            rows_to_clear.append(y)

    # Check for completed columns
    cols_to_clear = []
    for x in range(GRID_SIZE):
        if all(grid[y][x] != BLACK for y in range(GRID_SIZE)): #se toda a linha estiver cheia (aka colorida)
            cols_to_clear.append(x)

    # Clear completed rows
    for y in rows_to_clear:
        for x in range(GRID_SIZE):
            grid[y][x] = BLACK
        lines_cleared += 1 

    # Clear completed columns
    for x in cols_to_clear:
        for y in range(GRID_SIZE):
            grid[y][x] = BLACK
        lines_cleared += 1

    return lines_cleared #para poder contar pontos !

#õe um bloco aleatória na grid (para o que o objetivo possa ser atinjido em pc mode)
def place_random_block(grid, blocks):
    if not blocks:
        print("No blocks left to place!")
        return grid, blocks

    # Cria uma cópia da lista de blocos para evitar modificar a original durante o loop
    remaining_blocks = blocks.copy()

    while remaining_blocks:
        # Escolhe um bloco aleatório da lista de blocos restantes
        block, color = random.choice(remaining_blocks)
        rotations = get_rotations(block)

        # Tenta todas as rotações e posições para o bloco escolhido
        for rotation in rotations:
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid):
                        # Coloca o bloco na grade
                        place_block(rotation, x, y, color, grid)
                        # Remove o bloco da lista de blocos disponíveis
                        blocks.remove((block, color))
                        return grid, blocks

        # Se o bloco não puder ser colocado, remove-o da lista de blocos restantes
        remaining_blocks.remove((block, color))

    # Se nenhum bloco puder ser colocado após testar todos
    print("No valid placement found for any block!")
    return grid, blocks




#inutil depuis que goal changed ??? :
#Calcula o número de células vazias (ou disponíveis) na grid.
def heuristic_empty_cells(grid):
    return sum(cell == BLACK for row in grid for cell in row)

#Calcula o número de linhas completas na grade (ou seja, linhas que têm células vazias).
def heuristic_row_completion(grid):
    completed_rows = sum(all(cell == BLACK for cell in row) for row in grid)
    return - completed_rows

#inutil depuis que goal changed ??? :
#Combina duas métricas em uma única heurística: Minimiza o número de células vazias. Maximiza o número de linhas e colunas completas.
def combined_heuristic(grid):
    empty_cells = sum(cell == BLACK for row in grid for cell in row)
    completed_rows = sum(all(cell == BLACK for cell in row) for row in grid)
    completed_cols = sum(all(grid[y][x] == BLACK for y in range(GRID_SIZE)) for x in range(GRID_SIZE))
    return empty_cells - (completed_rows + completed_cols)  # Quanto menor o valor, melhor (menos células vazias e mais linhas/colunas completas).

def block_count_heuristic(grid, blocks):
    """
    Heuristic that prioritizes minimizing the number of remaining blocks.
    """
    return len(blocks)  # Fewer remaining blocks are better

#novas heuristics more appropriate for goal ?
#Conta o número de células preenchidas na grade. Quanto menor o valor, mais próxima a grade está de ficar vazia.
def heuristic_filled_cells(grid, blocks=None):  # Adicionamos um argumento opcional
    return sum(cell != BLACK for row in grid for cell in row)

#Conta o número de blocos restantes. Quanto menor o valor, mais próxima a grade está de ficar vazia.
def heuristic_remaining_blocks(blocks):
    return len(blocks)

#Combina a contagem de células preenchidas e blocos restantes.
def combined_heuristic_empty_grid(grid, blocks):
    filled_cells = sum(cell != BLACK for row in grid for cell in row)
    remaining_blocks = len(blocks)
    return filled_cells + remaining_blocks  # Minimize both

#Verifica quantos blocos podem ser removidos da grade. Quanto mais blocos forem removidos, mais próxima a grade está de ficar vazia.
def heuristic_block_removal(grid, blocks):
    removable_blocks = 0
    for block, color in blocks:
        for rotation in get_rotations(block):
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    if can_place_block(rotation, x, y, grid):
                        removable_blocks += 1
                        break
                else:
                    continue
                break
    return -removable_blocks  # Maximize removable blocks







def draw_grid(screen, grid):
    """
    Draw the grid on the screen.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) #A posição e o tamanho do  grid são calculados com base no tamanho do bloco 

def draw_blocks(screen, blocks):
    """
    Draw the available blocks on the screen. - mostrando ao jogador quais blocos ele pode colocar na grade.
    """
    for i, (block, color) in enumerate(blocks): #block = matriz 2D que representa o formato do bloco.
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    pygame.draw.rect(screen, color, (WIDTH - 150 + col * BLOCK_SIZE, 50 + row * BLOCK_SIZE + i * 100, BLOCK_SIZE, BLOCK_SIZE)) #A posição do bloco é calculada para que os blocos sejam exibidos à direita da grade (WIDTH - 150), com um espaçamento vertical entre eles (i * 100).

def render(screen, grid, blocks, score):
    """
    Render the entire game state (grid, blocks, and score).
    """
    screen.fill(WHITE) #o screen que abre
    draw_grid(screen, grid) #o grid onde se vai jogar
    draw_blocks(screen, blocks) #os blocos a jogar
    font = pygame.font.SysFont("Arial", 24) #para texto da pontação
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10)) 
    pygame.display.flip() #atualizar a tela com o conteúdo desenhado.








# Initialize Pygame
pygame.init() # Inicializa todos os módulos do Pygame (como gráficos, som, fontes, etc.).
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Cria a janela do jogo com o tamanho especificado (WIDTH de largura e HEIGHT de altura).
pygame.display.set_caption("Wood Block Puzzle") #Define o título da janela do jogo como "Wood Block Puzzle".

# Game setup
grid = [[BLACK for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] #Cria a grade do jogo como uma matriz 2D (lista de listas).
blocks = [generate_block() for _ in range(3)] #Cria uma lista de blocos iniciais para o jogo (pode se escolher um dos 3 propostos)
selected_block = None #Essa variável será usada para armazenar o bloco que o jogador selecionou para colocar na grade.
score = 0 #initializa os pontos a 0 






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








# Game modes
def pc_mode(algorithm, heuristic=None):
    global grid, blocks
    state = State(grid, blocks)  # Cria o estado inicial
    grid, blocks = place_random_block(grid, blocks)  # Coloca um bloco aleatório para iniciar
    start_time = time.time()  # Inicia o cronômetro
    visited_states = 0  # Contador de estados visitados

    while not state.is_goal():  # Enquanto o estado atual não for o objetivo
        if algorithm == "bfs":
            new_state = bfs(state)  # Executa BFS
        elif algorithm == "dfs":
            new_state = dfs(state)  # Executa DFS
        elif algorithm == "greedy":
            new_state = greedy(state, heuristic)  # Executa Greedy
        elif algorithm == "a_star":
            new_state = a_star(state, heuristic)  # Executa A*

        if new_state is None:  # Se nenhum estado válido for encontrado
            print("No solution found!")
            return

        state = new_state  # Atualiza o estado atual
        grid = [row[:] for row in state.grid]  # Atualiza a grid
        blocks = state.blocks  # Atualiza os blocos

        visited_states += 1  # Incrementa o contador de estados visitados
        print(f"Visited states: {visited_states}")  # Exibe o número de estados visitados
        print(f"Remaining blocks: {len(state.blocks)}")  # Exibe o número de blocos restantes
        print("Current grid:")  # Exibe a grade atual
        for row in state.grid:
            print(row)

        render(screen, state.grid, state.blocks, score)  # Renderiza a interface gráfica
        pygame.time.delay(500)  # Pausa de 500ms para visualização

    print(f"Puzzle solved in {time.time() - start_time:.2f} seconds!")  # Exibe o tempo total
    print(f"Visited states: {visited_states}")  # Exibe o número total de estados visitados



def human_mode():
    global selected_block, grid, blocks, score
    running = True  # Controla o loop principal do jogo
    dragging = False  # Indica se um bloco está sendo arrastado
    drag_pos = (0, 0)  # Posição do mouse durante o arrasto

    while running:  # Loop principal do jogo
        for event in pygame.event.get():  # Processa eventos do Pygame
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Se o botão do mouse for pressionado
                x, y = pygame.mouse.get_pos()
                if WIDTH - 150 <= x <= WIDTH - 50 and 50 <= y <= 350:  # Verifica se o clique foi na área dos blocos
                    selected_index = (y - 50) // 100  # Calcula o índice do bloco selecionado
                    selected_block = blocks[selected_index]  # Seleciona o bloco
                    dragging = True  # Inicia o arrasto
                    drag_pos = (x, y)  # Armazena a posição inicial do arrasto
            elif event.type == pygame.MOUSEBUTTONUP:  # Se o botão do mouse for solto
                if dragging and selected_block:  # Se um bloco estava sendo arrastado
                    grid_x, grid_y = drag_pos[0] // BLOCK_SIZE, drag_pos[1] // BLOCK_SIZE  # Converte a posição do mouse para coordenadas da grade
                    block, color = selected_block
                    if can_place_block(block, grid_x, grid_y, grid):  # Verifica se o bloco pode ser colocado
                        place_block(block, grid_x, grid_y, color, grid)  # Coloca o bloco na grade
                        lines_cleared = clear_completed_lines(grid)  # Limpa linhas completas
                        score += lines_cleared * 10  # Atualiza a pontuação
                        blocks[selected_index] = generate_block()  # Gera um novo bloco
                        selected_block = None  # Deseleciona o bloco
                        if all(cell != BLACK for row in grid for cell in row):  # Verifica se a grade está cheia
                            print("You win! Final Score:", score)
                            running = False
                    dragging = False  # Finaliza o arrasto
            elif event.type == pygame.MOUSEMOTION and dragging:  # Se o mouse estiver sendo movido durante o arrasto
                drag_pos = pygame.mouse.get_pos()  # Atualiza a posição do arrasto
            elif event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if event.key == pygame.K_SPACE:  # Se a tecla for espaço
                    if selected_block:  # Rotaciona o bloco selecionado
                        block, color = selected_block
                        rotated_block = list(zip(*block[::-1]))  # Rotaciona 90 graus
                        selected_block = (rotated_block, color) 

        if no_valid_moves_left(grid, blocks):  # Verifica se não há mais movimentos válidos
            print("No valid moves left! Game Over. Final Score:", score)
            running = False

        render(screen, grid, blocks, score)  # Renderiza a interface gráfica
        if dragging and selected_block:  # Se um bloco estiver sendo arrastado
            block, color = selected_block
            for row in range(len(block)):  # Desenha o bloco na posição do mouse
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (drag_pos[0] + col * BLOCK_SIZE, drag_pos[1] + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()  # Atualiza a tela

def human_mode():
    global selected_block, grid, blocks, score
    running = True  # Controla o loop principal do jogo
    dragging = False  # Indica se um bloco está sendo arrastado

    while running:  # Loop principal do jogo
        for event in pygame.event.get():  # Processa eventos do Pygame
            if event.type == pygame.QUIT:  # Se o usuário fechar a janela
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Se o botão do mouse for pressionado
                x, y = pygame.mouse.get_pos()
                # Verifica se o clique foi na área dos blocos disponíveis
                if WIDTH - 150 <= x <= WIDTH - 50 and 50 <= y <= 350:
                    selected_index = (y - 50) // 100  # Calcula o índice do bloco selecionado
                    selected_block = blocks[selected_index]  # Seleciona o bloco
                    dragging = True  # Inicia o arrasto
            elif event.type == pygame.MOUSEBUTTONUP:  # Se o botão do mouse for solto
                if dragging and selected_block:  # Se um bloco estava sendo arrastado
                    x, y = pygame.mouse.get_pos()
                    grid_x, grid_y = x // BLOCK_SIZE, y // BLOCK_SIZE  # Converte a posição do mouse para coordenadas da grade
                    block, color = selected_block
                    if can_place_block(block, grid_x, grid_y, grid):  # Verifica se o bloco pode ser colocado
                        place_block(block, grid_x, grid_y, color, grid)  # Coloca o bloco na grade
                        lines_cleared = clear_completed_lines(grid)  # Limpa linhas completas
                        score += lines_cleared * 10  # Atualiza a pontuação
                        blocks[selected_index] = generate_block()  # Gera um novo bloco
                        selected_block = None  # Deseleciona o bloco
                        if all(cell != BLACK for row in grid for cell in row):  # Verifica se a grade está cheia
                            print("You win! Final Score:", score)
                            running = False
                    dragging = False  # Finaliza o arrasto
            elif event.type == pygame.KEYDOWN:  # Se uma tecla for pressionada
                if event.key == pygame.K_SPACE:  # Se a tecla for espaço
                    if selected_block:  # Rotaciona o bloco selecionado
                        block, color = selected_block
                        rotated_block = list(zip(*block[::-1]))  # Rotaciona 90 graus
                        selected_block = (rotated_block, color)

        # Verifica se não há mais movimentos válidos
        if no_valid_moves_left(grid, blocks):
            print("No valid moves left! Game Over. Final Score:", score)
            running = False

        render(screen, grid, blocks, score)  # Renderiza a interface gráfica
        # Desenha o bloco selecionado sendo arrastado
        if dragging and selected_block:
            block, color = selected_block
            x, y = pygame.mouse.get_pos()
            # Desenha o bloco na posição do mouse
            for row in range(len(block)):
                for col in range(len(block[row])):
                    if block[row][col]:
                        pygame.draw.rect(screen, color, (x + col * BLOCK_SIZE, y + row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()  # Atualiza a tela



        

# Main function
def main():
    global GRID_SIZE, grid, blocks
    print("Welcome to Wood Block Puzzle!")
    print("1. PC Mode")
    print("2. Human Mode")
    mode = input("Select mode (1/2): ")  # Solicita ao usuário que escolha o modo
    if mode == "1":  # Modo PC
        print("1. BFS")
        print("2. DFS")
        print("3. Greedy")
        print("4. A*")
        algorithm = input("Select algorithm (1/2/3/4): ")  # Solicita ao usuário que escolha o algoritmo
        if algorithm == "1":
            pc_mode("bfs")
        elif algorithm == "2":
            pc_mode("dfs")
        elif algorithm == "3":
            pc_mode("greedy", heuristic_filled_cells)
        elif algorithm == "4":
            pc_mode("a_star", combined_heuristic_empty_grid)
    elif mode == "2":  # Modo Humano
        human_mode()
    pygame.quit()  # Encerra o Pygame

if __name__ == "__main__":
    main()