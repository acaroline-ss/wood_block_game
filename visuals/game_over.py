"""
Game Over Screen Module

Displays the game over screen with the player's final score and options to retry,
return to main menu, or quit the game. Features a dramatic visual style with
neon effects and button interactions.
"""

import pygame
from pathlib import Path
from cst import WIDTH, HEIGHT, TITLE_FONT
from visuals.buttons import Button

class GameOver:
    """
    Game Over screen that appears when the player loses the game.
    
    Attributes:
        screen (pygame.Surface): The display surface to draw on
        score (int): The player's final score to display
        background (pygame.Surface): The background image or fallback color
        buttons (list): Interactive buttons for player choices
    """
    
    def __init__(self, screen, score):
        """
        Initialize the Game Over screen.
        
        Args:
            screen (pygame.Surface): The game's display surface
            score (int): The player's final score
        """
        self.screen = screen
        self.score = score
        
        # Color definitions with descriptive names
        self.NEON_RED = (255, 50, 50)      # Vibrant red for title
        self.TEXT_WHITE = (255, 255, 255)   # White for text and outlines
        self.SCORE_COLOR = (255, 255, 255)  # White for score display
        self.BLACK = (0, 0, 0)              # Black for shadows
        
        # Load background image with fallback to solid color
        try:
            bg_path = Path(__file__).parent.parent / "assets" / "game_over_bg.png"
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background = pygame.Surface((WIDTH, HEIGHT))
            self.background.fill((40, 0, 0))  # Dark red fallback
        
        # Create title with outline effect
        self.title_text = "GAME OVER"
        self.title_main = TITLE_FONT.render(self.title_text, True, self.NEON_RED)
        self.title_outline = TITLE_FONT.render(self.title_text, True, self.TEXT_WHITE)
        self.title_rect = self.title_main.get_rect(center=(WIDTH//2, 100))
        
        # Score display font
        self.score_font = pygame.font.Font(None, 40)
        
        # Create action buttons
        self.buttons = [
            Button("Try Again", (WIDTH//2, 300), "retry", "game_over"),
            Button("Main Menu", (WIDTH//2, 380), "main_menu", "game_over"),
            Button("Quit", (WIDTH//2, 460), "quit", "game_over")
        ]

    def run(self):
        """
        Run the game over screen loop.
        
        Returns:
            str: The action selected by the player ("retry", "main_menu", or "quit")
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
        """Helper method to handle all drawing operations."""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title with outline effect (4 offset positions)
        for offset in [(-3,-3), (3,-3), (-3,3), (3,3)]:
            self.screen.blit(
                self.title_outline, 
                (self.title_rect.x + offset[0], self.title_rect.y + offset[1])
            )
        
        # Draw main title text
        self.screen.blit(self.title_main, self.title_rect)
        
        # Draw score
        score_text = self.score_font.render(
            f"Final Score: {self.score}", 
            True, 
            self.SCORE_COLOR
        )
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)