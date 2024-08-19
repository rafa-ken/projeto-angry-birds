import pygame
import math

class SlingshotController:
    def __init__(self, slingshot, bird):
        self.slingshot = slingshot
        self.bird = bird
        self.is_dragging = False
        self.mouse_position = (0, 0)

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_bird_in_sling():
                self.is_dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_dragging:
                self.is_dragging = False
                self.launch_bird()

    def handle_mouse_motion(self, event):
        if self.is_dragging:
            self.mouse_position = pygame.mouse.get_pos()
            self.update_bird_position()

    def is_bird_in_sling(self):
        bird_rect = pygame.Rect(self.bird_position[0], self.bird_position[1], self.bird.size, self.bird.size)
        return bird_rect.collidepoint(pygame.mouse.get_pos())

    def update_bird_position(self):
        sling_x, sling_y = self.slingshot.position
        mouse_x, mouse_y = self.mouse_position
        dx = mouse_x - sling_x
        dy = mouse_y - sling_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.slingshot.max_pull_distance:
            # Normalize the vector and scale it to the max pull distance
            dx = dx / distance * self.slingshot.max_pull_distance
            dy = dy / distance * self.slingshot.max_pull_distance

        # Update bird position based on the elastic effect
        self.bird_position = (sling_x + dx, sling_y + dy)

    def launch_bird(self):
        sling_x, sling_y = self.slingshot.position
        bird_x, bird_y = self.bird_position
        dx = bird_x - sling_x
        dy = bird_y - sling_y
        angle = math.degrees(math.atan2(-dy, dx))
        power = min(math.sqrt(dx ** 2 + dy ** 2), self.slingshot.max_pull_distance)

        # Launch the bird using the calculated angle and power
        self.slingshot.release_bird(angle, power)
