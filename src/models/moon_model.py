import pygame
import math

class Moon(pygame.sprite.Sprite):
    def __init__(self, x, y, mass=2300, radius=60):
        super().__init__()
        self.sprite_sheet = pygame.image.load("./resources/images/angry_birds.png").convert_alpha()
        moon_rect = pygame.Rect(0, 800, 350, 350)
        self.moon_image = self.sprite_sheet.subsurface(moon_rect)
        self.image = pygame.transform.scale(self.moon_image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.mass = mass
        self.radius = radius
        self.G = 1

    def apply_gravity(self, bird):
        if not bird.not_released:
            distance_x = self.rect.centerx - bird.rect.centerx
            distance_y = self.rect.centery - bird.rect.centery
            distance = math.hypot(distance_x, distance_y)

            if distance == 0:
                return

            force = self.G * (self.mass * bird.mass) / (distance ** 2)
            force_x = force * (distance_x / distance)
            force_y = force * (distance_y / distance)

            bird.velocity[0] += force_x
            bird.velocity[1] += force_y

    def handle_collision(self, bird):
        if self.rect.colliderect(bird.rect):
            bird_center = bird.rect.center
            moon_center = self.rect.center

            direction_x = bird_center[0] - moon_center[0]
            direction_y = bird_center[1] - moon_center[1]

            magnitude = math.hypot(direction_x, direction_y)
            if magnitude > 0:
                direction_x /= magnitude
                direction_y /= magnitude

            push_strength = 5
            bird.velocity[0] += direction_x * push_strength
            bird.velocity[1] += direction_y * push_strength
