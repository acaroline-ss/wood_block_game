#buttons.py
#Componentes de botão
import pygame
from cst import WIDTH, HEIGHT

class Button:
    def __init__(self, text, pos, action, width=200, height=50):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = text
        self.action = action
        self.colors = {
            "normal": (100, 70, 30),  # Marrom escuro
            "hover": (139, 69, 19)    # Marrom claro
        }

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.colors["hover"] if self.rect.collidepoint(mouse_pos) else self.colors["normal"]
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (50, 30, 10), self.rect, 2, border_radius=8)
        font = pygame.font.SysFont("Luckiest Guy", 24)
        text = font.render(self.text, True, (240, 220, 180))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False