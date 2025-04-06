# victory.py
import pygame
from pathlib import Path
from cst import WIDTH, HEIGHT, TITLE_FONT
from visuals.buttons import Button

class VictoryScreen:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        
        # Cores ajustadas
        self.GREEN_NEON = (57, 255, 20)      # Verde neon vibrante
        self.DARK_BROWN = (101, 67, 33)      # Marrom bem escuro
        self.BLACK = (0, 0, 0)               # Preto para borda
        
        # Carrega o background
        try:
            bg_path = Path(__file__).parent.parent / "assets" / "victory_bg.png"
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((25, 25, 112))
        
        # Prepara o título com borda preta
        self.title_text = "VOCÊ VENCEU!"
        self.title_main = TITLE_FONT.render(self.title_text, True, self.GREEN_NEON)
        self.title_outline = TITLE_FONT.render(self.title_text, True, self.BLACK)
        
        # Posição do título (centralizado)
        self.title_rect = self.title_main.get_rect(center=(WIDTH//2, 120))
        
        # Fonte da pontuação
        self.score_font = pygame.font.Font(None, 40)  # Aumentei para 40px
        
        # Botões
        self.buttons = [
            Button("Próximo Nível", (WIDTH//2, 320), "next_level", "victory"),
            Button("Menu Principal", (WIDTH//2, 420), "main_menu", "victory")
        ]

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            # Renderização
            self.screen.blit(self.background, (0, 0))
            
            # Desenha borda do título (em 4 posições para criar contorno)
            for offset in [(-2,-2), (2,-2), (-2,2), (2,2)]:
                self.screen.blit(self.title_outline, 
                               (self.title_rect.x + offset[0], 
                                self.title_rect.y + offset[1]))
            
            # Título principal
            self.screen.blit(self.title_main, self.title_rect)
            
            # Pontuação escura
            score_text = self.score_font.render(f"Pontuação Final: {self.score}", 
                                              True, self.DARK_BROWN)
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            
            # Botões
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()
            clock.tick(60)