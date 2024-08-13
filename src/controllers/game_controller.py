import pygame

from models import PlanetModel, BirdModel
from views import ScreenView, SpritesView

class GameController:
    def __init__(self):
        self.screen = ScreenView()
        self.planets = [
            PlanetModel("Earth", 12742, 5972000000000000000000000, 12742, 149600000, 0),
            PlanetModel("Mars", 6779, 639000000000000000000000, 6779, 227900000, 225000000)
        ]
        self.bird = BirdModel("Red", 10, 20, 50, "None")
        self.bird_position = [100, 300]
        self.bird_velocity = [0, 0]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def update(self):
        # Update bird physics
        self.bird_position[0] += self.bird_velocity[0]
        self.bird_position[1] += self.bird_velocity[1]
        self.bird_velocity[1] += 0.5

    def draw(self):
        self.screen.clear()
        for i, planet in enumerate(self.planets):
            SpritesView.draw_planet(self.screen.surface, planet, 300 + i*200, 300)
        SpritesView.draw_bird(self.screen.surface, self.bird, *self.bird_position)
        pygame.display.flip()

    def launch_bird(self, angle, power):
        import math
        self.bird_velocity[0] = math.cos(math.radians(angle)) * power
        self.bird_velocity[1] = -math.sin(math.radians(angle)) * power
