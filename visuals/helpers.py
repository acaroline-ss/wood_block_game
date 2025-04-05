# helpers.py
import pygame
from cst import *

def draw_button(screen, rect, text, font, hover=False):
    """Draw a styled button with hover effect on the given surface.
    
    Args:
        screen (pygame.Surface): The surface to draw the button on.
        rect (pygame.Rect): The rectangular area defining button position and size.
        text (str): The text to display on the button.
        font (pygame.font.Font): The font to use for the button text.
        hover (bool): Whether the button is in hover state. Defaults to False.
        
    Returns:
        pygame.Rect: The rectangle area of the drawn button (same as input rect).
        
    Note:
        Uses a wood-like color scheme with dark brown for normal state
        and lighter brown for hover state, matching the game's aesthetic.
    """
    # Choose color based on hover state - provides visual feedback
    color = (100, 70, 30) if hover else (70, 40, 10)  # Light vs dark brown
    
    # Draw the main button body with rounded corners
    pygame.draw.rect(screen, color, rect, border_radius=8)
    
    # Add a darker border to make the button stand out
    pygame.draw.rect(screen, (50, 30, 10), rect, 2, border_radius=8)

    # Render the button text in antique white for good contrast
    text_surface = font.render(text, True, (240, 220, 180))
    
    # Center the text within the button rectangle
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    # Return the rect for collision detection or positioning
    return rect


def draw_text(screen, text, size, x, y, color=WHITE):
    """Draw centered text on the given surface.
    
    Args:
        screen (pygame.Surface): The surface to draw the text on.
        text (str): The text content to display.
        size (int): Font size in pixels.
        x (int): X-coordinate for text center position.
        y (int): Y-coordinate for text center position.
        color (tuple): RGB color tuple for the text. Defaults to WHITE.
        
    Returns:
        pygame.Rect: The rectangular area occupied by the drawn text.
        
    Note:
        Uses pygame's default font. For consistent styling across the game,
        consider using a custom font loaded at game initialization.
    """
    # Create a font object with specified size
    font = pygame.font.Font(None, size)
    
    # Render the text with anti-aliasing for smooth edges
    text_surface = font.render(text, True, color)
    
    # Center the text at the specified (x,y) coordinates
    text_rect = text_surface.get_rect(center=(x, y))
    
    # Draw the text on the screen surface
    screen.blit(text_surface, text_rect)
    
    # Return the rect in case caller needs collision detection
    return text_rect