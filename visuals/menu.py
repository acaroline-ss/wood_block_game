# menu.py
"""Menu system for the Wood Block Puzzle game.

Contains all menu classes including:
- MainMenu: Primary game menu with core options
- GameModeMenu: Mode selection screen
- LevelMenu: Level selection interface

All menus follow consistent visual styling with wood-themed colors and fonts.
"""

import pygame
from cst import *
from visuals.buttons import Button

class MainMenu:
    """Handles the main menu screen and navigation.
    
    Attributes:
        screen (pygame.Surface): The game's display surface
        buttons (list): Collection of menu action buttons
    """
    
    def __init__(self, screen):
        """Initialize main menu with navigation options.
        
        Args:
            screen (pygame.Surface): Game display surface
        """
        self.screen = screen
        # Create vertically stacked buttons centered on screen
        # Each button has:
        # - Display text
        # - Position (centered horizontally with vertical spacing)
        # - Action string to return when clicked
        self.buttons = [
            Button("Jogar", (WIDTH//2-100, 200), "play"),          # Start game
            Button("Configurações", (WIDTH//2-100, 280), "settings"),  # Settings
            Button("Sobre", (WIDTH//2-100, 360), "about"),         # About screen
            Button("Sair", (WIDTH//2-100, 440), "quit")            # Exit game
        ]

    def run(self):
        """Run the main menu loop.
        
        Returns:
            str: Action identifier based on user selection:
                - "play": Start the game
                - "settings": Open settings
                - "about": Show about screen
                - "quit": Exit game
        """
        while True:
            # Fill with SaddleBrown color (RGB: 139, 69, 19)
            # This creates a warm wood-like background
            self.screen.fill((139, 69, 19))
            
            # Draw game title with decorative font
            # Using "Luckiest Guy" for playful, casual feel
            font = pygame.font.SysFont("Luckiest Guy", 64)
            title = font.render("Wood Block Puzzle", True, (240, 220, 180))  # Antique white
            # Center title horizontally near top of screen
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
            
            # Event handling loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"  # Window close button
                
                # Check button interactions
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action  # Return the button's action
            
            # Draw all buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            # Update display
            pygame.display.flip()


class GameModeMenu:
    """Handles game mode selection screen.
    
    Attributes:
        screen (pygame.Surface): Game display surface
        buttons (list): Mode selection options
    """
    
    def __init__(self, screen):
        """Initialize mode selection menu.
        
        Args:
            screen (pygame.Surface): Game display surface
        """
        self.screen = screen
        # Mode selection buttons with same layout as main menu
        self.buttons = [
            Button("Modo Humano", (WIDTH//2-100, 200), "human"),      # Human player
            Button("Modo PC", (WIDTH//2-100, 280), "pc"),            # AI player
            Button("Modo Assistido", (WIDTH//2-100, 360), "assistant"),  # Assisted play
            Button("Voltar", (WIDTH//2-100, 440), "back")             # Return to main
        ]

    def run(self):
        """Run the mode selection loop.
        
        Returns:
            str: Selected mode or navigation action:
                - "human": Human vs human mode
                - "pc": AI vs AI mode
                - "assistant": Human with AI hints
                - "back": Return to main menu
                - "quit": Exit game
        """
        while True:
            # Consistent background with main menu
            self.screen.fill((139, 69, 19))
            
            # Draw mode selection title
            font = pygame.font.SysFont("Luckiest Guy", 48)
            title = font.render("Selecione o Modo", True, (240, 220, 180))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            # Draw all buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()


class LevelMenu:
    """Handles level selection screen.
    
    Attributes:
        screen (pygame.Surface): Game display surface
        buttons (list): Level selection options
    """
    
    def __init__(self, screen):
        """Initialize level selection menu.
        
        Args:
            screen (pygame.Surface): Game display surface
        """
        self.screen = screen
        # Level buttons return level numbers (int) except back button
        self.buttons = [
            Button("Nível 1", (WIDTH//2-100, 200), 1),    # Level 1
            Button("Nível 2", (WIDTH//2-100, 280), 2),    # Level 2
            Button("Nível 3", (WIDTH//2-100, 360), 3),    # Level 3
            Button("Voltar", (WIDTH//2-100, 440), "back")  # Return
        ]

    def run(self):
        """Run the level selection loop.
        
        Returns:
            int/str: Selected level or navigation action:
                - 1-3: Selected level number
                - "back": Return to previous menu
                - "quit": Exit game
        """
        while True:
            # Consistent background
            self.screen.fill((139, 69, 19))
            
            # Draw level selection title
            font = pygame.font.SysFont("Luckiest Guy", 48)
            title = font.render("Selecione o Nível", True, (240, 220, 180))
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                for button in self.buttons:
                    if button.handle_event(event):
                        return button.action
            
            # Draw all buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            pygame.display.flip()