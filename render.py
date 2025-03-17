import pygame
from cst import *
from game import *

def draw_grid(screen, grid):
    """
    #Draw the grid on the screen.
    """
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)) #A posição e o tamanho do  grid são calculados com base no tamanho do bloco 

def draw_blocks(screen, blocks):
    """
    #Draw the available blocks on the screen. - mostrando ao jogador quais blocos ele pode colocar na grade.
    """
    for i, (block, color) in enumerate(blocks): #block = matriz 2D que representa o formato do bloco.
        for row in range(len(block)):
            for col in range(len(block[row])):
                if block[row][col]:
                    pygame.draw.rect(screen, color, (WIDTH - 150 + col * BLOCK_SIZE, 50 + row * BLOCK_SIZE + i * 100, BLOCK_SIZE, BLOCK_SIZE)) #A posição do bloco é calculada para que os blocos sejam exibidos à direita da grade (WIDTH - 150), com um espaçamento vertical entre eles (i * 100).

def render(screen, grid, blocks, score):
    """
    #Render the entire game state (grid, blocks, and score).
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