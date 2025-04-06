"""
Menu System Module

Provides all menu interfaces for the Wood Block Puzzle game including:
- Main menu
- Game mode selection
- Level selection
- Algorithm selection
- About screen

Features consistent styling, background management, and text rendering with outline effects.
All menus follow the same architectural pattern for maintainability.
"""

import pygame
from cst import WIDTH, HEIGHT, MENU_ASSETS
from visuals.buttons import Button

# Constants for consistent styling
TITLE_COLOR = (255, 180, 0)  # Gold color for titles
OUTLINE_COLOR = (0, 0, 0)     # Black for text outlines
OUTLINE_SIZE = 4               # Thickness of text outlines
BUTTON_SPACING = 90            # Vertical space between buttons
START_Y = 200                  # Starting Y position for first button

def render_text_with_outline(font, text, text_color=TITLE_COLOR, 
                           outline_color=OUTLINE_COLOR, outline_size=OUTLINE_SIZE):
    """
    Render text with an outline effect for better visibility against backgrounds.
    
    Args:
        font (pygame.Font): Font to use for rendering
        text (str): Text to display
        text_color (tuple): RGB color for main text
        outline_color (tuple): RGB color for outline
        outline_size (int): Thickness of outline in pixels
        
    Returns:
        pygame.Surface: Surface containing the rendered text with outline
    """
    text_surface = font.render(text, True, text_color)
    outline_surface = font.render(text, True, outline_color)
    
    # Create surface with extra space for outline
    combined = pygame.Surface(
        (text_surface.get_width() + outline_size*2, 
         text_surface.get_height() + outline_size*2), 
        pygame.SRCALPHA
    )
    
    # Draw outline in all directions
    offsets = [-outline_size, 0, outline_size]
    for x in offsets:
        for y in offsets:
            if x or y:  # Skip center position
                combined.blit(outline_surface, 
                            (outline_size + x, 
                             outline_size + y))
    
    # Draw main text centered
    combined.blit(text_surface, (outline_size, outline_size))
    return combined

class BackgroundManager:
    """
    Manages loading and displaying menu backgrounds with fallback support.
    Caches loaded backgrounds for better performance.
    """
    
    def __init__(self):
        """Preload all menu backgrounds during initialization."""
        self.backgrounds = {
            menu_type: self._load_bg(path)
            for menu_type, path in MENU_ASSETS.items()
            if menu_type.endswith("_bg")
        }
    
    def _load_bg(self, path):
        """
        Load and scale a background image.
        
        Args:
            path (str): Path to image file
            
        Returns:
            pygame.Surface: Scaled background or None if loading fails
        """
        try:
            bg = pygame.image.load(path).convert()
            return pygame.transform.scale(bg, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Error loading background {path}: {e}")
            return None
    
    def draw(self, screen, menu_type):
        """
        Draw the appropriate background for a menu type.
        
        Args:
            screen (pygame.Surface): Surface to draw on
            menu_type (str): Key for background type ("main", "modes", etc.)
        """
        bg = self.backgrounds.get(menu_type + "_bg", None)
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((139, 69, 19))  # Fallback wood brown

class BaseMenu:
    """
    Base class for all menus providing common functionality.
    Inherited by specific menu classes.
    """
    
    def __init__(self, screen, menu_type):
        """
        Initialize base menu properties.
        
        Args:
            screen (pygame.Surface): Game display surface
            menu_type (str): Type of menu for background selection
        """
        self.screen = screen
        self.menu_type = menu_type
        self.bg_manager = BackgroundManager()
        self.buttons = []
        self._init_fonts()
    
    def _init_fonts(self):
        """Initialize fonts with fallback support."""
        try:
            self.title_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 48)
            self.text_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 24)
        except:
            self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
            self.text_font = pygame.font.SysFont("Arial", 24)
    
    def _draw_title(self, title_text):
        """
        Draw menu title with consistent styling.
        
        Args:
            title_text (str): Text to display as title
        """
        title = render_text_with_outline(self.title_font, title_text, TITLE_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 70))
    
    def _handle_events(self):
        """
        Handle common menu events.
        
        Returns:
            str: Action from button press or None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            for button in self.buttons:
                if button.handle_event(event):
                    return button.action
        return None
    
    def _draw_buttons(self):
        """Draw all menu buttons."""
        for button in self.buttons:
            button.draw(self.screen)
    
    def run(self):
        """Base run method to be overridden by subclasses."""
        raise NotImplementedError("Subclasses must implement run()")

class MainMenu(BaseMenu):
    """Main game menu with play, about and quit options."""
    
    def __init__(self, screen):
        super().__init__(screen, "main")
        self.buttons = [
            Button("Play", (WIDTH//2, 250), "play"),
            Button("About", (WIDTH//2, 350), "about"),
            Button("Quit", (WIDTH//2, 450), "quit")
        ]
        self._init_title_fonts()
    
    def _init_title_fonts(self):
        """Special fonts for the main title."""
        try:
            self.big_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 72)
            self.small_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 36)
        except:
            self.big_font = pygame.font.SysFont("Arial", 72, bold=True)
            self.small_font = pygame.font.SysFont("Arial", 36, bold=True)
    
    def _draw_main_title(self):
        """Draw the hierarchical main game title."""
        # Main title part
        wood_block = render_text_with_outline(self.big_font, "WOOD BLOCK", TITLE_COLOR)
        wood_block_pos = (WIDTH//2 - wood_block.get_width()//2, 70)
        
        # Subtitle part
        game = render_text_with_outline(self.small_font, "GAME", TITLE_COLOR)
        game_pos = (WIDTH//2 - game.get_width()//2, 
                   wood_block_pos[1] + wood_block.get_height() - 15)
        
        self.screen.blit(wood_block, wood_block_pos)
        self.screen.blit(game, game_pos)
    
    def run(self):
        """Run the main menu loop."""
        while True:
            self.bg_manager.draw(self.screen, self.menu_type)
            self._draw_main_title()
            
            action = self._handle_events()
            if action:
                return action
            
            self._draw_buttons()
            pygame.display.flip()

class GameModeMenu(BaseMenu):
    """Menu for selecting game mode (human, PC, or assisted)."""
    
    def __init__(self, screen):
        super().__init__(screen, "modes")
        self.buttons = [
            Button("Human Mode", (WIDTH//2, START_Y), "human"),
            Button("PC Mode", (WIDTH//2, START_Y + BUTTON_SPACING), "pc"),
            Button("Assistant Mode", (WIDTH//2, START_Y + 2*BUTTON_SPACING), "assistant"),
            Button("Back", (WIDTH//2, START_Y + 3*BUTTON_SPACING), "back")
        ]
    
    def run(self):
        """Run the mode selection loop."""
        while True:
            self.bg_manager.draw(self.screen, self.menu_type)
            self._draw_title("Select Mode")
            
            action = self._handle_events()
            if action:
                return action
            
            self._draw_buttons()
            pygame.display.flip()

class LevelMenu(BaseMenu):
    """Menu for selecting game level (1-3)."""
    
    def __init__(self, screen):
        super().__init__(screen, "levels")
        self.buttons = [
            Button("Level 1", (WIDTH//2, START_Y), 1),
            Button("Level 2", (WIDTH//2, START_Y + BUTTON_SPACING), 2),
            Button("Level 3", (WIDTH//2, START_Y + 2*BUTTON_SPACING), 3),
            Button("Back", (WIDTH//2, START_Y + 3*BUTTON_SPACING), "back")
        ]
    
    def run(self):
        """Run the level selection loop."""
        while True:
            self.bg_manager.draw(self.screen, self.menu_type)
            self._draw_title("Select Level")
            
            action = self._handle_events()
            if action:
                return action
            
            self._draw_buttons()
            pygame.display.flip()

class AlgorithmMenu(BaseMenu):
    """Menu for selecting PC algorithm (BFS, DFS, Greedy, A*)."""
    
    def __init__(self, screen):
        super().__init__(screen, "algorithm")  # Changed to match background key
        self.buttons = [
            Button("BFS", (WIDTH//2, START_Y), "bfs"),
            Button("DFS", (WIDTH//2, START_Y + BUTTON_SPACING), "dfs"),
            Button("Greedy", (WIDTH//2, START_Y + 2*BUTTON_SPACING), "greedy"),
            Button("A*", (WIDTH//2, START_Y + 3*BUTTON_SPACING), "a_star"),
            Button("Back", (WIDTH//2, START_Y + 4*BUTTON_SPACING), "back")
        ]

    def run(self):
        """Run the algorithm selection loop."""
        while True:
            # Explicitly use "algorithm_bg" to match the assets dictionary
            self.bg_manager.draw(self.screen, "algorithm")  # This will use algorithm_bg
            self._draw_title("Select Algorithm")
            
            action = self._handle_events()
            if action:
                return action
            
            self._draw_buttons()
            pygame.display.flip()

class AboutMenu(BaseMenu):
    """About screen with game information and credits."""
    
    def __init__(self, screen):
        super().__init__(screen, "main")  # Uses main background
        self.menu_button = Button("Menu", (100, HEIGHT - 70), "back")
        self._init_content()
    
    def _init_content(self):
        """Initialize about screen text content."""
        self.about_text = [
            "Welcome to Wood Block Puzzle!",
            "",
            "Enjoy three game modes:",
            "- Human Mode: Full manual control",
            "- PC Mode: Watch AI algorithms solve levels",
            "- Assistant Mode: Get hints when you need help",
            "",
            "Score carefully!",
            "Fewer moves = higher scores!",
            "Hints cost precious points!",
            "",
            "Get ready for the challenge!"
        ]
        
        self.developers = [
            "Developed by:",
            "Alice de Azevedo Silva", 
            "Ana Carolina Soares Silva",
            "Beatriz Morais Vieira"
        ]
    
    def _draw_text_content(self):
        """Draw all text content on about screen."""
        # Main text
        y_offset = 150
        for line in self.about_text:
            if line:  # Skip empty lines (used as spacing)
                text = self.text_font.render(line, True, (255, 250, 250))
                self.screen.blit(text, (WIDTH//2 - text.get_width()//2, y_offset))
            y_offset += 30
        
        # Developers text (bottom right)
        dev_y = HEIGHT - len(self.developers) * 30 - 20
        for i, line in enumerate(self.developers):
            text = self.text_font.render(line, True, (230, 230, 230))
            self.screen.blit(text, (WIDTH - text.get_width() - 20, dev_y + i*30))
    
    def run(self):
        """Run the about screen loop."""
        while True:
            self.bg_manager.draw(self.screen, self.menu_type)
            self._draw_title("About")
            self._draw_text_content()
            self.menu_button.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if self.menu_button.handle_event(event):
                    return self.menu_button.action
            
            pygame.display.flip()