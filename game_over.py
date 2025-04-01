#game_over.py
#game_over.py
import pygame
from cst import *
from visuals.buttons import Button

class GameOver:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.buttons = [
            Button("Tentar Novamente", (WIDTH//2-150, 300), "retry"),
            Button("Menu Principal", (WIDTH//2-150, 380), "main_menu")
        ]

    def run(self):
        while True:
            # Fundo semi-transparente
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            # Texto "Game Over"
            title_font = pygame.font.SysFont("Luckiest Guy", 72)
            title = title_font.render("Game Over", True, (255, 80, 80))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
            
            # Exibe a pontuação
            score_font = pygame.font.SysFont("Luckiest Guy", 48)
            score_text = score_font.render(f"Pontuação: {self.score}", True, WHITE)
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))
            
            # Botões
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()