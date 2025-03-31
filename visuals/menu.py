#menu.py
import pygame
from cst import *
from visuals.buttons import Button

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button("Jogar", (WIDTH//2-100, 200), "play"),
            Button("Configurações", (WIDTH//2-100, 280), "settings"),
            Button("Sobre", (WIDTH//2-100, 360), "about"),
            Button("Sair", (WIDTH//2-100, 440), "quit")
        ]

    def run(self):
        while True:
            self.screen.fill((139, 69, 19))  # Fundo marrom
            
            # Título
            font = pygame.font.SysFont("Luckiest Guy", 64)
            title = font.render("Wood Block Puzzle", True, (240, 220, 180))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()

class GameModeMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button("Modo Humano", (WIDTH//2-100, 200), "human"),
            Button("Modo PC", (WIDTH//2-100, 280), "pc"),
            Button("Modo Assistido", (WIDTH//2-100, 360), "assistant"),
            Button("Voltar", (WIDTH//2-100, 440), "back")
        ]

    def run(self):
        while True:
            self.screen.fill((139, 69, 19))
            
            font = pygame.font.SysFont("Luckiest Guy", 48)
            title = font.render("Selecione o Modo", True, (240, 220, 180))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()

class LevelMenu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = [
            Button("Nível 1", (WIDTH//2-100, 200), 1),
            Button("Nível 2", (WIDTH//2-100, 280), 2),
            Button("Nível 3", (WIDTH//2-100, 360), 3),
            Button("Voltar", (WIDTH//2-100, 440), "back")
        ]

    def run(self):
        while True:
            self.screen.fill((139, 69, 19))
            
            font = pygame.font.SysFont("Luckiest Guy", 48)
            title = font.render("Selecione o Nível", True, (240, 220, 180))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()