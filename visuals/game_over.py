# game_over.py
import pygame
from cst import *
from visuals.buttons import Button

class GameOver:
    """Game Over screen displayed when the player loses the game.
    
    Handles the display of game over message, final score, and provides
    options to retry or return to main menu.
    
    Attributes:
        screen (pygame.Surface): The main game surface to draw on.
        score (int): The player's final score to display.
        buttons (list): List of interactive buttons for user actions.
    """
    
    def __init__(self, screen, score):
        """Initialize the Game Over screen.
        
        Args:
            screen (pygame.Surface): The main game display surface.
            score (int): The final score achieved by the player.
        """
        self.screen = screen
        self.score = score
        # Create action buttons centered horizontally on screen
        # Button positions are calculated relative to screen width for responsiveness
        # Action strings will be returned to determine game flow
        self.buttons = [
            Button("Tentar Novamente", (WIDTH//2-150, 300), "retry"),  # Retry button
            Button("Menu Principal", (WIDTH//2-150, 380), "main_menu")  # Main menu button
        ]

    def run(self):
        """Run the game over screen loop.
        
        Returns:
            str: The action to take after screen closes ("retry", "main_menu", or "quit").
        """
        while True:
            # Create a semi-transparent overlay to darken the game background
            # This helps the game over elements stand out while showing the final game state
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # SRCALPHA enables alpha
            overlay.fill((0, 0, 0, 180))  # Black with 180/255 transparency
            self.screen.blit(overlay, (0, 0))
            
            # Display "Game Over" title in red for strong visual impact
            # Using the same "Luckiest Guy" font for consistency with button text
            title_font = pygame.font.SysFont("Luckiest Guy", 72)
            title = title_font.render("Game Over", True, (255, 80, 80))  # Bright red color
            # Center the title horizontally using screen width
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
            
            # Display the player's final score
            # Slightly smaller font size than title for visual hierarchy
            score_font = pygame.font.SysFont("Luckiest Guy", 48)
            score_text = score_font.render(f"Pontuação: {self.score}", True, WHITE)
            # Center the score below the title
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))
            
            # Handle events - this is the main interaction loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"  # Quit the game if window is closed
                
                # Check for button clicks
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action  # Return the associated action
            
            # Draw all buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            # Update the display
            pygame.display.flip()