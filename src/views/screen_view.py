import pygame

class ScreenView:
    def __init__(self, width=800, height=600, title="Angry fcking bird", bg_color=(135, 206, 235)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)

    def clear(self):
        """Clear the screen with the background color."""
        self.surface.fill(self.bg_color)

    def draw(self, drawable_objects):
        """Draw all drawable objects on the screen."""
        self.clear()
        for obj in drawable_objects:
            obj.draw(self.surface)
        pygame.display.flip()

    def get_surface(self):
        """Return the surface for external drawing if needed."""
        return self.surface

    def update_display(self):
        """Update the display after drawing operations."""
        pygame.display.update()
