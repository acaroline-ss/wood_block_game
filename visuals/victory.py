"""
Victory Screen Module

Displays the victory screen when a player completes a level successfully.
Shows the player's score and provides options to proceed to the next level
or return to the main menu.
"""

import pygame
from pathlib import Path
from cst import WIDTH, HEIGHT, TITLE_FONT
from visuals.buttons import Button

class VictoryScreen:
    """
    Victory screen that appears when the player successfully completes a level.
    
    Attributes:
        screen (pygame.Surface): The display surface to draw on
        score (int): The player's final score
        background (pygame.Surface): The background image or fallback color
        buttons (list): Interactive buttons for player choices
    """
    
    # Color constants for consistent styling
    NEON_GREEN = (57, 255, 20)    # Vibrant neon green for title
    DARK_BROWN = (101, 67, 33)    # Dark brown for score text
    BLACK = (0, 0, 0)             # Black for outlines
    FALLBACK_BG_COLOR = (25, 25, 112)  # Dark blue fallback background
    
    def __init__(self, screen, score):
        """
        Initialize the victory screen.
        
        Args:
            screen (pygame.Surface): The game's display surface
            score (int): The player's final score
        """
        self.screen = screen
        self.score = score
        
        # Load background image with fallback
        self._load_background()
        
        # Prepare title with outline effect
        self._prepare_title()
        
        # Initialize fonts
        self.score_font = pygame.font.Font(None, 40)
        
        # Create action buttons
        self.buttons = [
            Button("Next Level", (WIDTH//2, 320), "next_level", "victory"),
            Button("Main Menu", (WIDTH//2, 420), "main_menu", "victory")
        ]

    def _load_background(self):
        """
        Load and scale the victory background image.
        Falls back to solid color if image loading fails.
        """
        try:
            bg_path = Path(__file__).parent.parent / "assets" / "victory_bg.png"
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Error loading victory background: {e}")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill(self.FALLBACK_BG_COLOR)

    def _prepare_title(self):
        """Create the victory title with outline effect."""
        self.title_text = "VICTORY!"
        self.title_main = TITLE_FONT.render(self.title_text, True, self.NEON_GREEN)
        self.title_outline = TITLE_FONT.render(self.title_text, True, self.BLACK)
        self.title_rect = self.title_main.get_rect(center=(WIDTH//2, 120))

    def _draw_title(self):
        """
        Draw the title with outline effect by rendering the outline
        in multiple offset positions.
        """
        # Draw outline in four diagonal positions
        for offset in [(-2,-2), (2,-2), (-2,2), (2,2)]:
            self.screen.blit(
                self.title_outline,
                (self.title_rect.x + offset[0], self.title_rect.y + offset[1])
            )
        # Draw main title
        self.screen.blit(self.title_main, self.title_rect)

    def _draw_score(self):
        """Draw the player's final score."""
        score_text = self.score_font.render(
            f"Final Score: {self.score}", 
            True, 
            self.DARK_BROWN
        )
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))

    def _draw_buttons(self):
        """Draw all interactive buttons."""
        for button in self.buttons:
            button.draw(self.screen)

    def run(self):
        """
        Run the victory screen loop.
        
        Returns:
            str: The action selected by the player ("next_level", "main_menu", or "quit")
        """
        clock = pygame.time.Clock()
        
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                # Check button clicks
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            # Rendering
            self._draw_screen()
            pygame.display.flip()
            clock.tick(60)  # Maintain 60 FPS

    def _draw_screen(self):
        """Handle all drawing operations for the victory screen."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title and score
        self._draw_title()
        self._draw_score()
        
        # Draw buttons
        self._draw_buttons()