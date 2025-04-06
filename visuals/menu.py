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
            "levels": self._load_bg(MENU_ASSETS["levels_bg"]),
            "algorithms": self._load_bg(MENU_ASSETS["algorithm_bg"])
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

class AlgorithmMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_manager = BackgroundManager()
        
        # Button configuration
        start_y = 200                  # Initial button height
        spacing = 90                  # Space between buttons
        
        self.buttons = [
            Button("BFS", (WIDTH//2, start_y), "bfs"),
            Button("DFS", (WIDTH//2, start_y + spacing), "dfs"),
            Button("Greedy", (WIDTH//2, start_y + 2*spacing), "greedy"),
            Button("A*", (WIDTH//2, start_y + 3*spacing), "a_star"),
            Button("Voltar", (WIDTH//2, start_y + 4*spacing), "back")
        ]

    def run(self):
        while True:
            self.bg_manager.draw(self.screen, "algorithms")
            
            FONT_STYLE = "fonts/LuckiestGuy-Regular.ttf"
            try:
                font = pygame.font.Font(FONT_STYLE, 48)  # Size 48
            except:
                font = pygame.font.SysFont("Arial", 48)  # Fallback if font fails
            title = render_text_with_outline(font, "Selecione o Algoritmo", (255, 180, 0))
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


class AboutMenu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_manager = BackgroundManager()
        self.menu_button = Button("Menu", (100, HEIGHT - 70), "back")

    def run(self):
        while True:
            self.bg_manager.draw(self.screen, "main")  # Using main background or you can add specific one
            
            # Title
            try:
                font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 48)
                small_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 20)
            except:
                font = pygame.font.SysFont("Arial", 48, bold=True)
                small_font = pygame.font.SysFont("Arial", 24, bold=True)

            title = render_text_with_outline(font, "Sobre o Jogo", (255, 250, 200))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))

            # Main text (wrapped)
            about_text = [
                "Bem-vindos ao Wood Block Puzzle!",
                "",
                "Divirta-se com três modos de jogo:",
                "- Modo Humano: controle total manual",
                "- Modo PC: algoritmos inteligentes "
                "  resolvem os níveis",
                "- Modo Assistente: "
                "  peça ajuda ao algoritmo quando precisar",
                "",
                "Cuidado com as pontuações!",
                "Menos movimentos = mais pontos!",
                "Dicas custam pontos preciosos!",
                "",
                "Prepare-se para o desafio e divirta-se!"
            ]

            # Render wrapped text
            y_offset = 150
            for line in about_text:
                if line:  # Skip empty lines (spacing)
                    text_surface = small_font.render(line, True, (255, 250, 250))
                    self.screen.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_offset))
                y_offset += 30

            # Developers text (bottom right) - Multi-line version
            dev_lines = [
                "Desenvolvido por:",
                "Alice de Azevedo Silva", 
                "Ana Carolina Soares Silva",
                "Beatriz Morais Vieira"
                ]
            
            # Calculate total height needed (4 lines × 30px spacing = 120px total)
            total_text_height = len(dev_lines) * 30
            dev_y = HEIGHT - total_text_height - 20 

            for i, line in enumerate(dev_lines):
                dev_text = small_font.render(line, True, (230, 230, 230))
                self.screen.blit(dev_text, (WIDTH - dev_text.get_width() - 20, dev_y + i*30))

            # Menu button
            self.menu_button.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if self.menu_button.handle_event(event):
                    return self.menu_button.action
            
            pygame.display.flip()