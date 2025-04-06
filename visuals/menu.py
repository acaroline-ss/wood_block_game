#menu.py
import pygame
from cst import *
from visuals.buttons import Button

def render_text_with_outline(font, text, text_color=(255, 180, 0), outline_color=(0, 0, 0), outline_size=4):
    """Renderiza texto com borda. Cores padrão: amarelo-alaranjado com borda preta"""
    text_surface = font.render(text, True, text_color)
    outline_surface = font.render(text, True, outline_color)
    
    # Cria uma superfície ligeiramente maior para acomodar a borda
    combined = pygame.Surface(
        (text_surface.get_width() + outline_size*2, text_surface.get_height() + outline_size*2), 
        pygame.SRCALPHA
    )
    
    # Desenha a borda em todas as direções
    for x in range(-outline_size, outline_size+1):
        for y in range(-outline_size, outline_size+1):
            if x != 0 or y != 0:  # Não desenha no centro
                combined.blit(outline_surface, (outline_size + x, outline_size + y))
    
    # Desenha o texto principal no centro
    combined.blit(text_surface, (outline_size, outline_size))
    
    return combined

# Adicione no início do menu.py
class BackgroundManager:
    def __init__(self):
        self.backgrounds = {
            "main": self._load_bg(MENU_ASSETS["main_bg"]),
            "modes": self._load_bg(MENU_ASSETS["modes_bg"]),
            "levels": self._load_bg(MENU_ASSETS["levels_bg"])
        }
    
    def _load_bg(self, path):
        try:
            bg = pygame.image.load(path).convert()
            return pygame.transform.scale(bg, (WIDTH, HEIGHT))
        except:
            return None
    
    def draw(self, screen, menu_type):
        bg = self.backgrounds.get(menu_type)
        if bg:
            # Redimensiona se necessário (opcional)
            bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((139, 69, 19))  # Fallback

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_manager = BackgroundManager()
        self.buttons = [
            Button("Jogar", (WIDTH//2,250), "play"),
            Button("Sobre", (WIDTH//2, 350), "about"),
            Button("Sair", (WIDTH//2,450), "quit")
        ]

    def run(self):
        while True:
            self.bg_manager.draw(self.screen, "main")
            
            # Título
    # ===== NOVO TÍTULO HIERARQUICO ===== #
            try:
                big_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 72)    # Fonte grande
                small_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 36)   # Fonte menor
            except:
                big_font = pygame.font.SysFont("Arial", 72, bold=True)             # Fallback
                small_font = pygame.font.SysFont("Arial", 36, bold=True)

            # Renderiza "WOOD BLOCK" grande
            wood_block = render_text_with_outline(big_font, "WOOD BLOCK", (255, 180, 0))
            wood_block_pos = (WIDTH//2 - wood_block.get_width()//2, 70)  # Posição Y ajustada

            # Renderiza "GAME" menor
            game = render_text_with_outline(small_font, "GAME", (255, 180, 0))
            game_pos = (WIDTH//2 - game.get_width()//2, wood_block_pos[1] + wood_block.get_height() - 15)

            # Desenha na tela
            self.screen.blit(wood_block, wood_block_pos)
            self.screen.blit(game, game_pos)
            # ===== FIM DO NOVO TÍTULO ===== #
            
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
        self.bg_manager = BackgroundManager()
        # Configurações de posição (ajuste apenas esses valores)
        start_y = 200                  # Altura inicial dos botões
        spacing = 90                   # Espaço entre botões

        self.buttons = [
            Button("Modo Humano", (WIDTH//2,start_y), "human"),
            Button("Modo PC", (WIDTH//2, start_y + spacing), "pc"),
            Button("Modo Assistente", (WIDTH//2, start_y + 2*spacing), "assistant"),
            Button("Voltar", (WIDTH//2, start_y + 3*spacing), "back")
        ]

    def run(self):
        while True:
            self.bg_manager.draw(self.screen, "modes")
            
            FONT_STYLE = "fonts/LuckiestGuy-Regular.ttf"
            try:
                font = pygame.font.Font(FONT_STYLE, 48)  # Tamanho 48
            except:
                font = pygame.font.SysFont("Arial", 48)  # Fallback se a fonte falhar
            title = render_text_with_outline(font, "Selecione o Modo", (255, 180, 0))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))
            
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
        self.bg_manager = BackgroundManager()

        start_y = 200                  # Altura inicial dos botões
        spacing = 90    

        self.buttons = [
            Button("Nível 1", (WIDTH//2,start_y), 1),
            Button("Nível 2", (WIDTH//2,start_y + spacing), 2),
            Button("Nível 3", (WIDTH//2, start_y + 2*spacing), 3),
            Button("Voltar", (WIDTH//2, start_y + 3*spacing), "back")
        ]

    def run(self):
        while True:
            self.bg_manager.draw(self.screen, "levels")
            
            FONT_STYLE = "fonts/LuckiestGuy-Regular.ttf"
            try:
                font = pygame.font.Font(FONT_STYLE, 48)  # Tamanho 48
            except:
                font = pygame.font.SysFont("Arial", 48)  # Fallback se a fonte falhar
            title = render_text_with_outline(font, "Selecione o Nível", (255, 180, 0))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip() 