# levels.py
"""Level selection menu for the wood block puzzle game.

This module handles the display and interaction with the level selection screen,
allowing players to choose which puzzle level to play or return to the main menu.
"""

import pygame
from cst import *

def show_level_menu(screen):
    """Display and manage the level selection menu.
    
    Args:
        screen (pygame.Surface): The game's main display surface.
        
    Returns:
        str/int: Returns either:
            - "quit" if the player closes the window
            - "back" if the back button is pressed
            - int (level number) if a level is selected
            
    Note:
        Uses a vertical list of buttons with consistent styling matching
        the game's wood-themed aesthetic. Buttons are centered horizontally
        with equal vertical spacing.
    """
    # Use the game's standard font for consistency
    font = pygame.font.SysFont("Luckiest Guy", 48)
    
    # Define level selection buttons with their properties
    # Each button has:
    # - Display text
    # - pygame.Rect defining position and size
    # - Associated action (level number or "back")
    buttons = [
        {"text": "Nível 1", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "level": 1},
        {"text": "Nível 2", "rect": pygame.Rect(WIDTH//2-100, 280, 200, 50), "level": 2}, 
        {"text": "Nível 3", "rect": pygame.Rect(WIDTH//2-100, 360, 200, 50), "level": 3},
        {"text": "Voltar", "rect": pygame.Rect(WIDTH//2-100, 440, 200, 50), "level": "back"}
    ]
    
    # Main menu loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"  # Signal to quit the game
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button was clicked
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["level"] == "back":
                            return "back"  # Return to main menu
                        else:
                            return btn["level"]  # Return selected level number
        
        # Clear screen and draw background (would typically be done here)
        # screen.fill(BG_COLOR)  # Uncomment if you have a background color
        
        # Draw title
        title_font = pygame.font.SysFont("Luckiest Guy", 72)
        title = title_font.render("Selecione o Nível", True, (100, 70, 30))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Draw all buttons with hover effects
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            # Determine if mouse is hovering over this button
            is_hover = btn["rect"].collidepoint(mouse_pos)
            draw_button(screen, btn["rect"], btn["text"], font, is_hover)
        
        pygame.display.flip()


def draw_button(screen, rect, text, font, hover=False):
    """Draw a styled button with hover effect.
    
    Args:
        screen (pygame.Surface): Surface to draw the button on.
        rect (pygame.Rect): Position and dimensions of the button.
        text (str): Text to display on the button.
        font (pygame.font.Font): Font to use for the button text.
        hover (bool): Whether to show hover state. Defaults to False.
        
    Note:
        Uses a wood-like color scheme with:
        - Dark brown (70, 40, 10) for normal state
        - Medium brown (100, 70, 30) for hover state
        - Darker brown (50, 30, 10) for border
        - Cream (240, 220, 180) for text
    """
    # Select color based on hover state
    color = (100, 70, 30) if hover else (70, 40, 10)
    
    # Draw button body with rounded corners
    pygame.draw.rect(screen, color, rect, border_radius=8)
    
    # Add decorative border
    pygame.draw.rect(screen, (50, 30, 10), rect, 2, border_radius=8)
    
    # Render and center text
    text_surface = font.render(text, True, (240, 220, 180))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)