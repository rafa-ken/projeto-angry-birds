import pygame
import math
from helpers import (
    vec_add,
    vec_sub,
    vec_scale,
    vec_rotate
)


class Polygon:
    def __init__(self, body_position, vertices, image):
        self.body_position = body_position
        self.vertices = vertices
        self.image = image
        self.body_angle = 0  # Initial angle of the polygon

    def update_angle(self, angle_increment):
        self.body_angle += angle_increment

    def draw(self, screen):
        p = self.to_pygame(self.body_position)
        angle_degrees = math.degrees(self.body_angle)
        rotated_image = pygame.transform.rotate(self.image, angle_degrees)
        offset = vec_scale(rotated_image.get_size(), 0.5)
        p = vec_sub(p, offset)
        screen.blit(rotated_image, (p[0], p[1]))

    def to_pygame(self, p):
        return [int(p[0]), int(p[1])]

    def get_transformed_vertices(self):
        transformed_vertices = []
        for vertex in self.vertices:
            rotated_vertex = vec_rotate(vertex, self.body_angle)
            transformed_vertex = vec_add(self.body_position, rotated_vertex)
            transformed_vertices.append(transformed_vertex)
        return transformed_vertices
