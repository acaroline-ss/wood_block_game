from cst import BLACK

def heuristic_empty_cells(grid):
    return sum(cell == BLACK for row in grid for cell in row)

def heuristic_row_completion(grid):
    completed_rows = sum(all(cell != BLACK for cell in row) for row in grid)
    return -completed_rows