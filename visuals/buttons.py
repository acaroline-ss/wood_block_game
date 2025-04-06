#buttons.py
#Componentes de botão
import pygame
from cst import*

class Button:
    def __init__(self, text, pos, action, menu_type="main", selected=False):
        self.text = text
        self.action = action
        self.font = SUBTITLE_FONT  # Usa a fonte centralizada de cst.py
        # Aumente as dimensões padrão dos botões
        self.base_width = 250  # Aumentei de 200 para 280
        self.base_height = 100   # Aumentei de 50 para 70
        self.rect = pygame.Rect(0, 0, self.base_width, self.base_height)
        self.rect.center = pos
        
        # Carrega a imagem com novo tamanho
        if menu_type == "main":
            img_path = MENU_ASSETS["tabua1"]
        elif menu_type == "modes":
            img_path = MENU_ASSETS["tabua1"] 
        else:
            img_path = MENU_ASSETS["tabua1"]
            
        self.normal_img = self._load_img(img_path, self.base_width, self.base_height)
        self.hover_img = None
        self.selected = selected


    def _load_img(self, path, width, height):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (width, height))
        except Exception as e:
            print(f"Erro ao carregar {path}: {e}")
            return None

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.normal_img:
            surface.blit(self.normal_img, self.rect)
        else:
            color = (100, 70, 30) if self.rect.collidepoint(mouse_pos) else (70, 40, 10)
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            
                # Adiciona borda se selecionado
        if self.selected:
            pygame.draw.rect(surface, (255, 215, 0), self.rect, 3, border_radius=8)

        # Texto centralizado no novo tamanho
        text = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        
        # Adicione sombra para melhor legibilidade
        shadow = self.font.render(self.text, True, (50, 50, 50))
        surface.blit(shadow, (text_rect.x+2, text_rect.y+2))
        surface.blit(text, text_rect)



    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False