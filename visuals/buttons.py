# buttons.py
import pygame
from cst import WIDTH, HEIGHT

class Button:
    """A clickable button UI element for pygame applications.
    
    Attributes:
        rect (pygame.Rect): The rectangular area occupied by the button.
        text (str): The text displayed on the button.
        action (function): The callback function to execute when clicked.
        colors (dict): Color schemes for different button states.
    """
    
    def __init__(self, text, pos, action, width=200, height=50):
        """Initialize a Button instance.
        
        Args:
            text (str): Display text for the button.
            pos (tuple): (x, y) position coordinates for top-left corner.
            action (function): Callback to execute when button is clicked.
            width (int): Width of the button in pixels. Defaults to 200.
            height (int): Height of the button in pixels. Defaults to 50.
        """
        # Create a rectangular area for the button at given position and size
        # Using pygame.Rect makes collision detection and positioning easier
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = text
        self.action = action
        # Color scheme: Different colors for normal and hover states
        # Using earthy brown tones to match a wood block puzzle theme
        self.colors = {
            "normal": (100, 70, 30),  # Dark brown - normal state
            "hover": (139, 69, 19)     # Light brown - hover state (SaddleBrown)
        }

    def draw(self, surface):
        """Draw the button on the given surface.
        
        Args:
            surface (pygame.Surface): The game surface to draw the button on.
        """
        # Get mouse position to determine hover state
        mouse_pos = pygame.mouse.get_pos()
        
        # Change color if mouse is hovering over the button
        # This provides visual feedback to the player
        color = self.colors["hover"] if self.rect.collidepoint(mouse_pos) else self.colors["normal"]
        
        # Draw the main button rectangle with rounded corners
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        
        # Draw a darker border around the button for better visibility
        # The border helps define the button edges clearly
        pygame.draw.rect(surface, (50, 30, 10), self.rect, 2, border_radius=8)
        
        # Prepare the button text with a playful font
        # "Luckiest Guy" font was chosen for its casual, game-appropriate style
        font = pygame.font.SysFont("Luckiest Guy", 24)
        
        # Render text with an antique white color for good contrast on brown
        text = font.render(self.text, True, (240, 220, 180))
        
        # Center the text within the button rectangle
        text_rect = text.get_rect(center=self.rect.center)
        
        # Draw the text on the button
        surface.blit(text, text_rect)

    def handle_event(self, event):
        """Handle pygame events for button interaction.
        
        Args:
            event (pygame.Event): The event to handle.
            
        Returns:
            bool: True if the button was clicked, False otherwise.
        """
        # Check for mouse click events within the button area
        # This is the core interaction mechanism for the button
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            # Return True to indicate the button was clicked
            # The calling code can then execute the button's action
            return True
        return False