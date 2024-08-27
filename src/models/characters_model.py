import pymunk as pm
from pymunk import Vec2d
import pygame
import math


class Bird:
    def __init__(self, force, angle, xo, yo, space):
        self.not_released = True  # Bird starts as not released
        mass = 1
        radius = 15
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        self.body = pm.Body(mass, inertia)
        self.body.position = xo, yo
        self.shape = pm.Circle(self.body, radius)
        self.shape.elasticity = 0.95
        self.shape.friction = 0.9
        space.add(self.body, self.shape)
        self.velocity = [force * math.cos(angle), force * math.sin(angle)]
        self.body.apply_impulse_at_local_point(self.velocity)
        
        # Set up the rect attribute for drawing and collision handling
        self.image = pygame.image.load("./resources/images/red-bird3.png").convert_alpha()
        self.rect = self.image.get_rect(center=(xo, yo))

    def update_rect(self):
        """Update the rect position based on the bird's physics body."""
        self.rect.center = (int(self.body.position.x), int(600 - self.body.position.y))  # Convert pymunk coordinates to pygame coordinates

    def release(self):
        """Set the bird to released state."""
        self.not_released = False


class Pig():
    def __init__(self, x, y, space):
        self.life = 20
        mass = 5
        radius = 14
        inertia = pm.moment_for_circle(mass, 0, radius, (0, 0))
        body = pm.Body(mass, inertia)
        body.position = x, y
        shape = pm.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 1
        space.add(body, shape)
        self.body = body
        self.shape = shape
