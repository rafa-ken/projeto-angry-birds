import pygame
import math
from models import PlanetModel, BirdModel, SlingshotModel, ObstacleModel
from views import ScreenView, SpritesView
from controllers import SlingshotController

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
        self.bird_launched = False

        self.slingshot = SlingshotModel((100, 400), 0.8, 100)
        self.obstacles = [
            ObstacleModel((500, 300), (50, 100), 100),
            ObstacleModel((600, 250), (60, 120), 150)
        ]

        self.slingshot_controller = SlingshotController(self.slingshot, self.bird)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            self.slingshot_controller.handle_click(event)
            self.slingshot_controller.handle_mouse_motion(event)
        return True

    def update(self):
        if self.bird_launched:
            # Update bird physics only if the bird has been launched
            self.bird_position[0] += self.bird_velocity[0]
            self.bird_position[1] += self.bird_velocity[1]
            self.bird_velocity[1] += 0.5  # Gravity effect

            # Check for collisions with obstacles
            for obstacle in self.obstacles:
                if self.bird_collision(obstacle):
                    obstacle.take_damage(self.bird.weight)
                    # Handle bird damage here if necessary

    def draw(self):
        self.screen.clear()
        for i, planet in enumerate(self.planets):
            SpritesView.draw_planet(self.screen.surface, planet, 300 + i * 200, 300)
        SpritesView.draw_bird(self.screen.surface, self.bird, *self.bird_position)

        # Draw slingshot
        SpritesView.draw_slingshot(self.screen.surface, self.slingshot)

        # Draw obstacles
        for obstacle in self.obstacles:
            SpritesView.draw_obstacle(self.screen.surface, obstacle)

        pygame.display.flip()

    def launch_bird(self, angle, power):
        if not self.bird_launched:
            self.bird_velocity[0] = math.cos(math.radians(angle)) * power
            self.bird_velocity[1] = -math.sin(math.radians(angle)) * power
            self.bird_launched = True  # Set the flag to indicate the bird has been launched

    def bird_collision(self, obstacle):
        bird_rect = pygame.Rect(self.bird_position[0], self.bird_position[1], self.bird.size, self.bird.size)
        obstacle_rect = pygame.Rect(obstacle.position[0], obstacle.position[1], obstacle.size[0], obstacle.size[1])
        return bird_rect.colliderect(obstacle_rect)
