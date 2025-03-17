from cst import GRID_SIZE, BLACK, SHAPES, COLORS
from heuristics import heuristic_empty_cells
import random 

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
