import pygame
import math

class PolygonModel:
    def __init__(self, vertices, position=(0, 0), color=(255, 255, 255)):
        self.vertices = vertices
        self.position = position
        self.color = color

    def draw(self, screen):
        # Draw the polygon on the given screen
        pygame.draw.polygon(screen, self.color, self.get_absolute_vertices())

    def get_absolute_vertices(self):
        # Calculate the absolute positions of the vertices based on the polygon's position
        return [(v[0] + self.position[0], v[1] + self.position[1]) for v in self.vertices]

    def move(self, dx, dy):
        # Move the polygon by dx, dy
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def rotate(self, angle):
        # Rotate the polygon by the given angle
        cos_theta = math.cos(math.radians(angle))
        sin_theta = math.sin(math.radians(angle))
        self.vertices = [
            (
                cos_theta * v[0] - sin_theta * v[1],
                sin_theta * v[0] + cos_theta * v[1]
            )
            for v in self.vertices
        ]

    def check_collision(self, other_polygon):
        # Basic placeholder for collision detection with another polygon
        # This could be replaced with a more sophisticated algorithm
        return pygame.Rect(self.position, (50, 50)).colliderect(pygame.Rect(other_polygon.position, (50, 50)))
