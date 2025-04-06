#levels.py
#Gerenciamento de levels
import pygame
from cst import *
# No seu main.py (após show_main_menu e antes de main())

def show_level_menu(screen):
    font = pygame.font.SysFont("Luckiest Guy", 48)
    buttons = [
        {"text": "Nível 1", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "level": 1},
        {"text": "Nível 2", "rect": pygame.Rect(WIDTH//2-100, 280, 200, 50), "level": 2}, 
        {"text": "Nível 3", "rect": pygame.Rect(WIDTH//2-100, 360, 200, 50), "level": 3},
        {"text": "Voltar", "rect": pygame.Rect(WIDTH//2-100, 440, 200, 50), "level": "back"}
    ]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Mantém o mesmo
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["level"] == "back":
                            return "back"  # Retorna como string
                        else:
                            return btn["level"]  # Retorna o número do nível diretamente
                        
def draw_button(screen, rect, text, font, hover=False):
    color = (100, 70, 30) if hover else (70, 40, 10)  # Marrom claro/escuro
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, (50, 30, 10), rect, 2, border_radius=8)  # Borda
    
    text_surface = font.render(text, True, (240, 220, 180))  # Texto creme
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)