"""
Level Selection Menu Module

Provides a level selection interface where players can choose which game level to play
or return to the previous menu. Handles user input and visual presentation of level options.
"""

import pygame
from cst import WIDTH

def show_level_menu(screen):
    """
    Display and manage the level selection menu.
    
    Args:
        screen (pygame.Surface): The game display surface
        
    Returns:
        int|str: The selected level number (1-3) or "back"/"quit" for menu actions
    """
    # Initialize font and button definitions
    font = pygame.font.SysFont("Luckiest Guy", 48)
    
    # Button configuration: text, position, and associated level/action
    buttons = [
        {"text": "Level 1", "rect": pygame.Rect(WIDTH//2-100, 200, 200, 50), "level": 1},
        {"text": "Level 2", "rect": pygame.Rect(WIDTH//2-100, 280, 200, 50), "level": 2},
        {"text": "Level 3", "rect": pygame.Rect(WIDTH//2-100, 360, 200, 50), "level": 3},
        {"text": "Back", "rect": pygame.Rect(WIDTH//2-100, 440, 200, 50), "level": "back"}
    ]
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check button clicks
                for btn in buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["level"]  # Return the level number or action
        
        # Draw the menu
        _draw_level_menu(screen, font, buttons)
        pygame.display.flip()

def _draw_level_menu(screen, font, buttons):
    """
    Helper function to render the level selection menu.
    
    Args:
        screen (pygame.Surface): Display surface to draw on
        font (pygame.Font): Font to use for text
        buttons (list): List of button configurations
    """
    # Draw background (you may want to add a proper background image)
    screen.fill((139, 69, 19))  # Wooden brown background
    
    # Draw title
    title = font.render("Select Level", True, (240, 220, 180))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Draw buttons with hover effects
    mouse_pos = pygame.mouse.get_pos()
    for btn in buttons:
        is_hovered = btn["rect"].collidepoint(mouse_pos)
        _draw_menu_button(
            screen=screen,
            rect=btn["rect"],
            text=btn["text"],
            font=font,
            hover=is_hovered
        )

def _draw_menu_button(screen, rect, text, font, hover=False):
    """
    Draw a menu button with consistent styling.
    
    Args:
        screen (pygame.Surface): Surface to draw on
        rect (pygame.Rect): Button position and dimensions
        text (str): Button text
        font (pygame.Font): Font to use
        hover (bool): Whether the button is being hovered
    """
    # Button colors
    button_color = (100, 70, 30) if hover else (70, 40, 10)  # Light/dark brown
    border_color = (50, 30, 10)  # Darker brown border
    text_color = (240, 220, 180)  # Cream colored text
    
    # Draw button and border
    pygame.draw.rect(screen, button_color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)
    
    # Draw centered text
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)