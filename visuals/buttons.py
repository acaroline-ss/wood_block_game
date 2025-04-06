"""
Button Component Module

This module provides a Button class for creating interactive UI buttons in Pygame.
Buttons support hover effects, selection states, and custom actions.
"""

import pygame
from cst import *

class Button:
    """
    A customizable button component for Pygame applications.
    
    Attributes:
        text (str): The text displayed on the button
        action: The action/return value when button is clicked
        font (pygame.Font): Font used for button text
        rect (pygame.Rect): The button's position and dimensions
        normal_img (pygame.Surface): Default button appearance
        hover_img (pygame.Surface): Hover state appearance (optional)
        selected (bool): Whether the button is in selected state
    """
    
    def __init__(self, text, pos, action, menu_type="main", selected=False):
        """
        Initialize a Button instance.
        
        Args:
            text (str): Text to display on button
            pos (tuple): (x,y) position to center the button
            action: Value to return when button is clicked
            menu_type (str): Button style ("main", "modes", etc.)
            selected (bool): Initial selected state
        """
        self.text = text
        self.action = action
        self.font = SUBTITLE_FONT  # Use centralized font from constants
        
        # Set button dimensions - larger than standard for better visibility
        self.base_width = 250  
        self.base_height = 100
        self.rect = pygame.Rect(0, 0, self.base_width, self.base_height)
        self.rect.center = pos  # Position the button center at given coordinates
        
        # Load appropriate button image based on menu type
        img_path = MENU_ASSETS["tabua1"]  # Default wooden board image
        
        self.normal_img = self._load_img(img_path, self.base_width, self.base_height)
        self.hover_img = None  # Could be implemented for hover effects
        self.selected = selected  # Track selection state

    def _load_img(self, path, width, height):
        """
        Helper method to load and scale button images.
        
        Args:
            path (str): Path to image file
            width (int): Target width
            height (int): Target height
            
        Returns:
            pygame.Surface: Scaled image or None if loading fails
        """
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (width, height))
        except Exception as e:
            print(f"Error loading {path}: {e}")
            return None

    def draw(self, surface):
        """
        Draw the button on the given surface.
        
        Args:
            surface (pygame.Surface): The surface to draw on
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw button background - use image if available, otherwise fallback to colored rectangle
        if self.normal_img:
            surface.blit(self.normal_img, self.rect)
        else:
            # Fallback appearance - color changes on hover
            color = (100, 70, 30) if self.rect.collidepoint(mouse_pos) else (70, 40, 10)
            pygame.draw.rect(surface, color, self.rect, border_radius=8)
            
        # Highlight if button is selected (gold border)
        if self.selected:
            pygame.draw.rect(surface, (255, 215, 0), self.rect, 3, border_radius=8)

        # Render and position text
        text = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        
        # Add text shadow for better readability
        shadow = self.font.render(self.text, True, (50, 50, 50))
        surface.blit(shadow, (text_rect.x+2, text_rect.y+2))
        surface.blit(text, text_rect)

    def handle_event(self, event):
        """
        Handle pygame events for button interaction.
        
        Args:
            event (pygame.Event): The event to handle
            
        Returns:
            bool: True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
            if self.rect.collidepoint(event.pos):
                return True
        return False