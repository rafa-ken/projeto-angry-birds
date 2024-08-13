import pygame

class SpritesView:
    @staticmethod
    def draw_planet(surface, planet, x, y):
        radius = int(float(planet.diameter) / 2)
        color = (0, 255, 0)
        pygame.draw.circle(surface, color, (x, y), radius)

    @staticmethod
    def draw_bird(surface, bird, x, y):
        radius = 10
        color = (255, 0, 0)
        pygame.draw.circle(surface, color, (x, y), radius)
