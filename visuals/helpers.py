#helpers
import pygame
def draw_button(screen, rect, text, font, hover=False):
    color = (100, 70, 30) if hover else (70, 40, 10)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, (50, 30, 10), rect, 2, border_radius=8)
    
    text_surface = font.render(text, True, (240, 220, 180))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)