# game_over.py
import pygame
from pathlib import Path
from cst import WIDTH, HEIGHT, TITLE_FONT
from visuals.buttons import Button

class GameOver:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        
        # Cores personalizadas
        self.RED_NEON = (255, 50, 50)       # Vermelho vibrante
        self.BROWN = (255, 255, 255)          # Marrom escuro (igual ao Victory)
        self.WHITE = (255, 255, 255)        # Branco para borda
        self.BLACK = (0, 0, 0)              # Preto para sombra
        
        # Carrega o background
        try:
            bg_path = Path(__file__).parent.parent / "assets" / "game_over_bg.png"
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except:
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((40, 0, 0))  # Vermelho escuro fallback
        
        # Prepara o título com borda branca
        self.title_text = "GAME OVER! LOSER!!!"
        self.title_main = TITLE_FONT.render(self.title_text, True, self.RED_NEON)
        self.title_outline = TITLE_FONT.render(self.title_text, True, self.WHITE)
        self.title_rect = self.title_main.get_rect(center=(WIDTH//2, 100))
        
        # Fonte da pontuação
        self.score_font = pygame.font.Font(None, 40)
        
        # Botões centralizados
        self.buttons = [
            Button("Tentar Novamente", (WIDTH//2, 300), "retry", "game_over"),
            Button("Menu Principal", (WIDTH//2, 380), "main_menu", "game_over"),
            Button("Sair", (WIDTH//2, 460), "quit", "game_over")
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
            
            # Desenha borda branca ao redor do título (4 posições)
            for offset in [(-3,-3), (3,-3), (-3,3), (3,3)]:
                self.screen.blit(self.title_outline, 
                               (self.title_rect.x + offset[0], 
                                self.title_rect.y + offset[1]))
            
            # Título principal
            self.screen.blit(self.title_main, self.title_rect)
            
            # Pontuação branco
            score_text = self.score_font.render(f"Pontuação Final: {self.score}", 
                                              True, self.BROWN)
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            
            # Botões
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()
            clock.tick(60)