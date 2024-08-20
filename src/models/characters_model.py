import pygame
import math

class Bird:
    def __init__(self, distance, angle, x, y, space):
        self.life = 20
        mass = 5
        radius = 12
        inertia = mass * radius ** 2
        self.body_position = [x, y]
        self.body_velocity = [0, 0]
        power = distance * 53
        impulse = vec_rotate([power, 0], -angle)
        self.apply_impulse(impulse)
        self.shape_radius = radius
        self.shape_elasticity = 0.95
        self.shape_friction = 1
        space.append(self)

    def apply_impulse(self, impulse):
        # Assuming a simple model where impulse directly translates to velocity change
        self.body_velocity = vec_add(self.body_velocity, vec_scale(impulse, 1/5))

    def update_position(self, dt):
        # Update the position based on velocity and time step
        self.body_position = vec_add(self.body_position, vec_scale(self.body_velocity, dt))

    def draw(self, screen):
        p = self.to_pygame(self.body_position)
        angle_degrees = math.degrees(math.atan2(self.body_velocity[1], self.body_velocity[0]))
        rotated_image = pygame.transform.rotate(self.image, angle_degrees)
        offset = vec_scale(rotated_image.get_size(), 0.5)
        p = vec_sub(p, offset)
        screen.blit(rotated_image, (p[0], p[1]))

    def to_pygame(self, p):
        return [int(p[0]), int(p[1])]
