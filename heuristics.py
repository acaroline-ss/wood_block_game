from cst import *
from game import *

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
    #Heuristic that prioritizes minimizing the number of remaining blocks.
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
