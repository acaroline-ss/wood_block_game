"""
UI Helper Functions

Provides utility functions for drawing common UI elements like buttons and text
with consistent styling throughout the game.
"""

import pygame
from cst import *

def draw_button(screen, rect, text, font, hover=False):
    """
    Draw a styled button with hover effects and centered text.
    
    Args:
        screen (pygame.Surface): Surface to draw the button on
        rect (pygame.Rect): Position and dimensions of the button
        text (str): Text to display on the button
        font (pygame.Font): Font to use for the button text
        hover (bool): Whether the button is in hover state
        
    Returns:
        pygame.Rect: The button's rectangle (for collision detection)
    """
    # Button colors - brown shades with highlight on hover
    button_color = (100, 70, 30) if hover else (70, 40, 10)
    border_color = (50, 30, 10)
    text_color = (240, 220, 180)  # Light beige for text
    
    # Draw button background and border
    pygame.draw.rect(screen, button_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)

    # Render and position text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

    return rect

def draw_text(screen, text, size, x, y, color=WHITE):
    """
    Draw centered text on the screen with a specified font size and color.
    
    Args:
        screen (pygame.Surface): Surface to draw the text on
        text (str): Text to display
        size (int): Font size in pixels
        x (int): X position for center of text
        y (int): Y position for center of text
        color (tuple): RGB color tuple (defaults to white)
        
    Returns:
        pygame.Rect: The text's rectangle (for positioning/collision)
    """
    # Create a temporary font for this text
    font = pygame.font.Font(None, size)
    
    # Render and position the text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
    return text_rect