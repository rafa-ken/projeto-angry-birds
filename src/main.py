import os
import math
import time
import pygame
import pymunk as pm
from models import Bird, Pig, Moon
from controllers import Level
from helpers import (
    vector,
    unit_vector,
    distance
)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 650))
        pygame.display.set_caption("Angry Birds with Corpo gordo")
        self.clock = pygame.time.Clock()
        self.running = True
        self.space = pm.Space()
        self.space.gravity = (0.0, -700.0)

        # Load images
        self.redbird = pygame.image.load("./resources/images/red-bird3.png").convert_alpha()
        self.background = pygame.image.load("./resources/images/background3.png").convert_alpha()
        self.sling_image = pygame.image.load("./resources/images/sling-3.png").convert_alpha()
        self.buttons = pygame.image.load("./resources/images/selected-buttons.png").convert_alpha()
        self.pig_happy = pygame.image.load("./resources/images/pig_failed.png").convert_alpha()
        self.pig_happy = pygame.transform.scale(self.pig_happy, (50, 50))
        self.stars = pygame.image.load("./resources/images/stars-edited.png").convert_alpha()

        # Subsurfaces for star images
        self.star1 = self.stars.subsurface(pygame.Rect(0, 0, 200, 200)).copy()
        self.star2 = self.stars.subsurface(pygame.Rect(204, 0, 200, 200)).copy()
        self.star3 = self.stars.subsurface(pygame.Rect(426, 0, 200, 200)).copy()

        # Buttons
        self.pause_button = self.buttons.subsurface(pygame.Rect(164, 10, 60, 60)).copy()
        self.replay_button = self.buttons.subsurface(pygame.Rect(24, 4, 100, 100)).copy()
        self.next_button = self.buttons.subsurface(pygame.Rect(142, 365, 130, 100)).copy()
        self.play_button = self.buttons.subsurface(pygame.Rect(18, 212, 100, 100)).copy()

        # Game state variables
        self.score = 0
        self.game_state = 0
        self.bird_path = []
        self.mouse_pressed = False
        self.sling_x, self.sling_y = 135, 450
        self.sling2_x, self.sling2_y = 160, 450
        self.bold_font = pygame.font.SysFont("arial", 30, bold=True)
        self.bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
        self.bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
        self.rope_length = 90  # Add the rope length to fix the missing attribute

        # Initialize game objects
        self.pigs = []
        self.birds = []
        self.columns = []
        self.beams = []
        self.moon = Moon(600, 300)  # Initialize the moon with position and mass

        # Static floor
        self.static_body = pm.Body(body_type=pm.Body.STATIC)
        self.space.add(self.static_body)  # Add the static body to the space first

        self.static_lines = [pm.Segment(self.static_body, (0.0, 60.0), (1200.0, 60.0), 0.0)]
        for line in self.static_lines:
            line.elasticity = 0.95
            line.friction = 1
            line.collision_type = 3
            self.space.add(line)  # Now, add the lines

        # Initialize level
        self.level = Level(self.pigs, self.columns, self.beams, self.space, self.moon)
        self.level.number = 0
        self.level.load_level()

        # Set collision handlers
        self.space.add_collision_handler(0, 1).post_solve = self.post_solve_bird_pig
        self.space.add_collision_handler(0, 2).post_solve = self.post_solve_bird_wood
        self.space.add_collision_handler(1, 2).post_solve = self.post_solve_pig_wood

    def run(self):
        running = True
        while running:
            self.handle_events()
            self.x_mouse, self.y_mouse = pygame.mouse.get_pos()
            self.update()
            self.draw_game()
            pygame.display.flip()
            self.clock.tick(60)

    def update(self):
        birds_to_remove = []
        pigs_to_remove = []

        for bird in self.birds:
            bird.update_rect()  # Update bird rect
            if bird.shape.body.position.y < 0:
                birds_to_remove.append(bird)

        for pig in self.pigs:
            if pig.shape.body.position.y < 0:
                pigs_to_remove.append(pig)

        for bird in birds_to_remove:
            self.space.remove(bird.shape, bird.shape.body)
            self.birds.remove(bird)

        for pig in pigs_to_remove:
            self.space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

        # Physics update
        dt = 1.0 / 50.0 / 2.0
        for _ in range(2):
            self.space.step(dt)

        # Apply gravity from the moon
        for bird in self.birds:
            self.moon.apply_gravity(bird)
            self.moon.handle_collision(bird)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                # Toggle wall
                pass  # Implement wall toggle logic here
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.space.gravity = (0.0, -10.0)
                self.level.bool_space = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                self.space.gravity = (0.0, -700.0)
                self.level.bool_space = False
            elif pygame.mouse.get_pressed()[0]:
                self.mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.release_bird()

    def release_bird(self):
        if self.level.number_of_birds > 0:
            self.level.number_of_birds -= 1
            # Logic for releasing the bird
            mouse_distance = distance(self.sling_x, self.sling_y, self.x_mouse, self.y_mouse)
            angle = math.atan2(self.y_mouse - self.sling_y, self.x_mouse - self.sling_x)
            xo = 154
            yo = 156

            if mouse_distance > self.rope_length:
                mouse_distance = self.rope_length

            if self.x_mouse < self.sling_x + 5:
                bird = Bird(mouse_distance, angle, xo, yo, self.space)
            else:
                bird = Bird(-mouse_distance, angle, xo, yo, self.space)

            self.birds.append(bird)

            if self.level.number_of_birds == 0:
                self.t2 = time.time()

            self.mouse_pressed = False

    def draw_game(self):
        # Clear the screen and draw the background
        self.screen.fill((130, 200, 100))  # Fill with a solid color (background)
        self.screen.blit(self.background, (0, -50))  # Draw the background image

        # Draw the first part of the slingshot (behind the bird)
        rect_behind = pygame.Rect(50, 0, 70, 220)
        self.screen.blit(self.sling_image, (138, 420), rect_behind)

        # Draw all static objects (e.g., blocks and beams)
        for column in self.columns:
            column.draw_poly('columns', self.screen)
        for beam in self.beams:
            beam.draw_poly('beams', self.screen)

        # Draw the moon (big yellow bird)
        self.screen.blit(self.moon.image, self.moon.rect.topleft)

        # Draw the birds near the slingshot (waiting to be launched)
        if self.level.number_of_birds > 0:
            for i in range(self.level.number_of_birds - 1):
                x = 100 - (i * 35)
                self.screen.blit(self.redbird, (x, 508))

        # Draw all birds that are in flight
        for bird in self.birds:
            self.screen.blit(bird.image, bird.rect.topleft)

        # Draw all pigs
        for pig in self.pigs:
            pig_pos = pig.shape.body.position
            pig_rect = self.pig_happy.get_rect(center=(int(pig_pos.x), int(-pig_pos.y + 600)))
            self.screen.blit(self.pig_happy, pig_rect.topleft)

        # Handle bird slingshot interaction
        if self.mouse_pressed and self.level.number_of_birds > 0:
            self.sling_action()

        # Draw the second part of the slingshot (in front of the bird)
        rect_front = pygame.Rect(0, 0, 60, 200)
        self.screen.blit(self.sling_image, (120, 420), rect_front)

        # Draw additional elements like score, UI, etc.
        score_font = self.bold_font.render("SCORE", 1, (255, 255, 255))
        number_font = self.bold_font.render(str(self.score), 1, (255, 255, 255))
        self.screen.blit(score_font, (1060, 90))
        self.screen.blit(number_font, (1060, 130))

        # Update the display
        pygame.display.flip()



    def sling_action(self):
        v = vector((self.sling_x, self.sling_y), (self.x_mouse, self.y_mouse))
        uv = unit_vector(v)
        mouse_distance = distance(self.sling_x, self.sling_y, self.x_mouse, self.y_mouse)

        if mouse_distance > self.rope_length:
            pull_position = (uv[0] * self.rope_length + self.sling_x, uv[1] * self.rope_length + self.sling_y)
        else:
            pull_position = (self.x_mouse, self.y_mouse)

        bird_pos = (pull_position[0] - 20, pull_position[1] - 20)
        self.screen.blit(self.redbird, bird_pos)

        pygame.draw.line(self.screen, (0, 0, 0), (self.sling2_x, self.sling2_y), pull_position, 5)
        pygame.draw.line(self.screen, (0, 0, 0), (self.sling_x, self.sling_y), pull_position, 5)

    def post_solve_bird_pig(self, arbiter, space, _):
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body

        pigs_to_remove = []
        for pig in self.pigs:
            if pig_body == pig.body:
                pig.life -= 20
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
                    self.score += 10000

        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

    def post_solve_bird_wood(self, arbiter, space, _):
        poly_to_remove = []
        if arbiter.total_impulse.length > 1100:
            a, b = arbiter.shapes
            for column in self.columns:
                if b == column.shape:
                    poly_to_remove.append(column)
            for beam in self.beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)

            for poly in poly_to_remove:
                if poly in self.columns:
                    self.columns.remove(poly)
                if poly in self.beams:
                    self.beams.remove(poly)
            space.remove(b, b.body)
            self.score += 5000

    def post_solve_pig_wood(self, arbiter, space, _):
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in self.pigs:
                if pig_shape == pig.shape:
                    pig.life -= 20
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
                        self.score += 10000

        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

    def restart(self):
        for pig in self.pigs[:]:
            self.space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

        for bird in self.birds[:]:
            self.space.remove(bird.shape, bird.shape.body)
            self.birds.remove(bird)

        for column in self.columns[:]:
            self.space.remove(column.shape, column.shape.body)
            self.columns.remove(column)

        for beam in self.beams[:]:
            self.space.remove(beam.shape, beam.shape.body)
            self.beams.remove(beam)

        self.score = 0
        self.bird_path = []
        self.level.load_level()

if __name__ == "__main__":
    game = Game()
    game.run()
