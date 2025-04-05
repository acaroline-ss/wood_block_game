import pygame
from cst import *
from visuals.buttons import Button

class VictoryScreen:
    """Victory screen displayed when the player successfully completes a level.
    
    Shows congratulatory message, final score, and provides navigation options.
    
    Attributes:
        screen (pygame.Surface): The main game display surface
        score (int): The player's achieved score
        buttons (list): List of action buttons for navigation
    """
    
    def __init__(self, screen, score):
        """Initialize the victory screen.
        
        Args:
            screen (pygame.Surface): The game's main display surface
            score (int): The final score the player achieved
        """
        self.screen = screen
        self.score = score
        # Create navigation buttons centered horizontally with vertical spacing
        # Button positions calculated relative to screen width for responsiveness
        self.buttons = [
            Button("Próximo Nível", (WIDTH//2-150, 300), "next_level"),  # Continue to next level
            Button("Menu Principal", (WIDTH//2-150, 380), "main_menu")   # Return to main menu
        ]
        

    def run(self):
        """Run the victory screen loop.
        
        Returns:
            str: The action to take after screen closes:
                - "next_level": Proceed to next level
                - "main_menu": Return to main menu
                - "quit": Quit the game
                
        Displays:
            - Semi-transparent overlay over game background
            - Victory message in green
            - Final score in white
            - Navigation buttons with hover effects
        """
        while True:
            # Create semi-transparent overlay to dim the background
            # This makes victory elements stand out while showing completed level
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # SRCALPHA enables transparency
            overlay.fill((0, 0, 0, 180))  # Black with 70% opacity (180/255)
            self.screen.blit(overlay, (0, 0))
            
            # Display victory message in bright green for positive feedback
            title_font = pygame.font.SysFont("Luckiest Guy", 72)  # Playful, bold font
            title = title_font.render("Você Venceu!", True, (100, 255, 100))  # Light green
            # Center title horizontally
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))
            
            # Display final score in white for clear readability
            score_font = pygame.font.SysFont("Luckiest Guy", 48)  # Slightly smaller than title
            score_text = score_font.render(f"Pontuação Final: {self.score}", True, WHITE)
            # Center score below title
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"  # Quit if window closed
                
                # Check for button clicks
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action  # Return corresponding action
            
            # Draw all buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            # Update display
            pygame.display.flip()