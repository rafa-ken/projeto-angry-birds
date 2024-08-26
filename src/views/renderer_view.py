import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render(self, game_objects):
        """Render all game objects to the screen."""
        self.screen.fill((255, 255, 255))  # Clear the screen with a white background

        for obj in game_objects:
            obj.draw(self.screen)

        pygame.display.flip()  # Update the full display surface to the screen
