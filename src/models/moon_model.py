import pymunk
import math

class MoonModel(pymunk.Body):
    def __init__(self, mass, position):
        """
        Initialize the MoonModel as a static body with gravitational influence.
        :param mass: The mass of the moon.
        :param position: The position of the moon as a tuple (x, y).
        """
        super().__init__(mass=mass, moment=pymunk.inf)
        self.position = position
        self.mass = mass

    def gravitational_force(self, body):
        """
        Calculate the gravitational force exerted on a body.
        :param body: The pymunk body affected by the moon's gravity.
        :return: The gravitational force as a pymunk.Vec2d.
        """
        # Vector from the body to the moon
        direction = self.position - body.position
        distance = direction.length

        # Prevent division by zero or extremely close distances
        if distance < 1.0:
            distance = 1.0

        # Gravitational constant G is set to 1 for simplicity
        G = 1.0
        force_magnitude = G * (self.mass * body.mass) / (distance ** 2)

        # Normalize the direction and scale by the force magnitude
        force = direction.normalized() * force_magnitude
        return force
