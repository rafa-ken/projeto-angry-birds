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

    @staticmethod
    def draw_slingshot(surface, slingshot):
        color = (139, 69, 19)  # Brown color for the slingshot
        pygame.draw.line(surface, color, slingshot.position, (slingshot.position[0] - 50, slingshot.position[1] + 50), 5)
        pygame.draw.line(surface, color, slingshot.position, (slingshot.position[0] + 50, slingshot.position[1] + 50), 5)

        # Draw the loaded bird if any
        if slingshot.loaded_bird:
            bird_position = slingshot.position
            SpritesView.draw_bird(surface, slingshot.loaded_bird, bird_position[0], bird_position[1])

    @staticmethod
    def draw_obstacle(surface, obstacle):
        color = (139, 69, 19)  # Brown color for the obstacle
        pygame.draw.rect(surface, color, pygame.Rect(obstacle.position[0], obstacle.position[1], obstacle.size[0], obstacle.size[1]))
