import os
import pygame
import pymunk as pm
from models import Bird, Pig, Moon
from controllers import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 650))
        pygame.display.set_caption("Angry Birds with Gravity")
        self.clock = pygame.time.Clock()
        self.running = True
        self.space = pm.Space()
        self.space.gravity = (0.0, -700.0)

        # Load images
        self.sprite_sheet = pygame.image.load("./resources/images/angry_birds.png").convert_alpha()
        moon_rect = pygame.Rect(0, 800, 350, 350)
        self.moon_image = self.sprite_sheet.subsurface(moon_rect)
        self.big_bird= pygame.transform.scale(self.moon_image, (4600, 120))
        self.redbird = pygame.image.load("./resources/images/red-bird3.png").convert_alpha()
        self.background = pygame.image.load("./resources/images/background3.png").convert_alpha()
        self.sling_image = pygame.image.load("./resources/images/sling-3.png").convert_alpha()
        self.buttons = pygame.image.load("./resources/images/selected-buttons.png").convert_alpha()
        self.pig_happy = pygame.image.load("./resources/images/pig_failed.png").convert_alpha()
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
        while self.running:
            self.handle_events()
            self.update_game()
            self.draw_game()
            self.clock.tick(50)
            pygame.display.set_caption(f"fps: {self.clock.get_fps()}")

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
            # Logic for releasing the bird, similar to the original code
            self.mouse_pressed = False

    def update_game(self):
        dt = 1.0 / 50.0 / 2.0
        for x in range(2):
            self.space.step(dt)  # Update physics
        # Add moon gravity
        for bird in self.birds:
            self.moon.apply_gravity(bird)
            self.moon.handle_collision(bird)

    def draw_game(self):
        # Clear the screen and draw the background
        self.screen.fill((130, 200, 100))  # Fill with a solid color (background)
        self.screen.blit(self.background, (0, -50))  # Draw the background image

        # Draw all static objects (e.g., blocks and beams)
        for column in self.columns:
            column.draw_poly('columns', self.screen)
        for beam in self.beams:
            beam.draw_poly('beams', self.screen)

        # Draw the moon (as a pygame sprite)
        self.screen.blit(self.big_bird, (600, 300))

        # Draw all birds
        for bird in self.birds:
            bird_pos = bird.shape.body.position
            bird_rect = self.redbird.get_rect(center=(int(bird_pos.x), int(-bird_pos.y + 600)))
            self.screen.blit(self.redbird, bird_rect.topleft)

        # Draw all pigs
        for pig in self.pigs:
            pig_pos = pig.shape.body.position
            pig_rect = self.pig_happy.get_rect(center=(int(pig_pos.x), int(-pig_pos.y + 600)))
            self.screen.blit(self.pig_happy, pig_rect.topleft)

        # Draw the slingshot (if applicable)
        rect = pygame.Rect(50, 0, 70, 220)
        self.screen.blit(self.sling_image, (138, 420), rect)

        # Draw additional elements like score, UI, etc.
        score_font = self.bold_font.render("SCORE", 1, (255, 255, 255))
        number_font = self.bold_font.render(str(self.score), 1, (255, 255, 255))
        self.screen.blit(score_font, (1060, 90))
        self.screen.blit(number_font, (1060, 130))

        # Update the display
        pygame.display.flip()

    def post_solve_bird_pig(self, arbiter, space, _):
        """Handles the collision between a bird and a pig."""
        a, b = arbiter.shapes
        bird_body = a.body
        pig_body = b.body

        # Find the pig involved in the collision
        pigs_to_remove = []
        for pig in self.pigs:
            if pig_body == pig.body:
                pig.life -= 20
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
                    self.score += 10000  # Increase score

        # Remove the pig from space and the list if it's dead
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

    def post_solve_bird_wood(self, arbiter, space, _):
        """Handles the collision between a bird and wood (columns/beams)."""
        poly_to_remove = []
        if arbiter.total_impulse.length > 1100:
            a, b = arbiter.shapes
            for column in self.columns:
                if b == column.shape:
                    poly_to_remove.append(column)
            for beam in self.beams:
                if b == beam.shape:
                    poly_to_remove.append(beam)

            # Remove the impacted wood (columns/beams)
            for poly in poly_to_remove:
                if poly in self.columns:
                    self.columns.remove(poly)
                if poly in self.beams:
                    self.beams.remove(poly)
            space.remove(b, b.body)
            self.score += 5000  # Increase score

    def post_solve_pig_wood(self, arbiter, space, _):
        """Handles the collision between a pig and wood (columns/beams)."""
        pigs_to_remove = []
        if arbiter.total_impulse.length > 700:
            pig_shape, wood_shape = arbiter.shapes
            for pig in self.pigs:
                if pig_shape == pig.shape:
                    pig.life -= 20
                    if pig.life <= 0:
                        pigs_to_remove.append(pig)
                        self.score += 10000  # Increase score

        # Remove the pig if its life drops to zero
        for pig in pigs_to_remove:
            space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

    def restart(self):
        # Remove all pigs
        for pig in self.pigs[:]:
            self.space.remove(pig.shape, pig.shape.body)
            self.pigs.remove(pig)

        # Remove all birds
        for bird in self.birds[:]:
            self.space.remove(bird.shape, bird.shape.body)
            self.birds.remove(bird)

        # Remove all columns
        for column in self.columns[:]:
            self.space.remove(column.shape, column.shape.body)
            self.columns.remove(column)

        # Remove all beams
        for beam in self.beams[:]:
            self.space.remove(beam.shape, beam.shape.body)
            self.beams.remove(beam)

        # Reset score and game state
        self.score = 0
        self.bird_path = []
        self.level.load_level()

if __name__ == "__main__":
    game = Game()
    game.run()
