import os
import sys
import math
import time
import pygame
from models import Bird, Pig, Polygon
from controllers import Level

# Initialize Pygame and screen
pygame.init()
screen = pygame.display.set_mode((1200, 650))

# Load images and resources
redbird = pygame.image.load("./resources/images/red-bird3.png").convert_alpha()
background2 = pygame.image.load("./resources/images/background3.png").convert_alpha()
sling_image = pygame.image.load("./resources/images/sling-3.png").convert_alpha()
full_sprite = pygame.image.load("./resources/images/full-sprite.png").convert_alpha()
rect = pygame.Rect(181, 1050, 50, 50)
cropped = full_sprite.subsurface(rect).copy()
pig_image = pygame.transform.scale(cropped, (30, 30))
buttons = pygame.image.load("./resources/images/selected-buttons.png").convert_alpha()
pig_happy = pygame.image.load("./resources/images/pig_failed.png").convert_alpha()
stars = pygame.image.load("./resources/images/stars-edited.png").convert_alpha()
rect = pygame.Rect(0, 0, 200, 200)
star1 = stars.subsurface(rect).copy()
rect = pygame.Rect(204, 0, 200, 200)
star2 = stars.subsurface(rect).copy()
rect = pygame.Rect(426, 0, 200, 200)
star3 = stars.subsurface(rect).copy()
rect = pygame.Rect(164, 10, 60, 60)
pause_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(24, 4, 100, 100)
replay_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(142, 365, 130, 100)
next_button = buttons.subsurface(rect).copy()
rect = pygame.Rect(18, 212, 100, 100)
play_button = buttons.subsurface(rect).copy()

# Initialize game clock
clock = pygame.time.Clock()

# Initialize custom physics space
game_space = []  # List to store all game objects

# Define global game variables
pigs = []
birds = []
balls = []
polys = []
beams = []
columns = []
poly_points = []
ball_number = 0
polys_dict = {}
mouse_distance = 0
rope_length = 90
angle = 0
x_mouse = 0
y_mouse = 0
count = 0
mouse_pressed = False
t1 = 0
tick_to_next_circle = 10
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
sling_x, sling_y = 135, 450
sling2_x, sling2_y = 160, 450
score = 0
game_state = 0
bird_path = []
counter = 0
restart_counter = False
bonus_score_once = True
bold_font = pygame.font.SysFont("arial", 30, bold=True)
bold_font2 = pygame.font.SysFont("arial", 40, bold=True)
bold_font3 = pygame.font.SysFont("arial", 50, bold=True)
wall = False

# Static floor setup (replacing pymunk segments with custom logic)
def create_static_floor(space):
    # Define the floor as a simple horizontal line
    floor = {'start': (0, 600), 'end': (1200, 600), 'elasticity': 0.95, 'friction': 1}
    wall = {'start': (1200, 600), 'end': (1200, 800), 'elasticity': 0.95, 'friction': 1}
    space.append(floor)
    space.append(wall)

create_static_floor(game_space)

def to_pygame(p):
    """Convert game coordinates to pygame coordinates."""
    return int(p[0]), int(-p[1] + 600)

def vector(p0, p1):
    """Return the vector between two points."""
    a = p1[0] - p0[0]
    b = p1[1] - p0[1]
    return [a, b]

def unit_vector(v):
    """Return the unit vector of the vector v."""
    h = (v[0]**2 + v[1]**2) ** 0.5
    if h == 0:
        h = 1e-15  # Prevent division by zero
    ua = v[0] / h
    ub = v[1] / h
    return [ua, ub]

def distance(xo, yo, x, y):
    """Calculate the distance between two points."""
    dx = x - xo
    dy = y - yo
    return (dx ** 2 + dy ** 2) ** 0.5

def load_music():
    """Load and play the background music."""
    song1 = '../resources/sounds/angry-birds.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)

def sling_action():
    """Handle the slingshot mechanics."""
    global mouse_distance, rope_length, angle, x_mouse, y_mouse

    # Calculate the vector from the sling to the mouse position
    v = vector((sling_x, sling_y), (x_mouse, y_mouse))
    uv = unit_vector(v)
    uv1, uv2 = uv

    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pu = (uv1 * rope_length + sling_x, uv2 * rope_length + sling_y)
    bigger_rope = 102
    x_redbird = x_mouse - 20
    y_redbird = y_mouse - 20

    if mouse_distance > rope_length:
        pux, puy = pu
        pux -= 20
        puy -= 20
        pul = pux, puy
        screen.blit(redbird, pul)
        pu2 = (uv1 * bigger_rope + sling_x, uv2 * bigger_rope + sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu2, 5)
        screen.blit(redbird, pul)
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu2, 5)
    else:
        mouse_distance += 10
        pu3 = (uv1 * mouse_distance + sling_x, uv2 * mouse_distance + sling_y)
        pygame.draw.line(screen, (0, 0, 0), (sling2_x, sling2_y), pu3, 5)
        screen.blit(redbird, (x_redbird, y_redbird))
        pygame.draw.line(screen, (0, 0, 0), (sling_x, sling_y), pu3, 5)

    # Calculate the angle for launching the bird
    dy = y_mouse - sling_y
    dx = x_mouse - sling_x
    if dx == 0:
        dx = 1e-15  # Prevent division by zero
    angle = math.atan(dy / dx)

def draw_level_cleared():
    """Display the 'Level Cleared' screen and award bonus points."""
    global game_state, bonus_score_once, score

    level_cleared = bold_font3.render("Level Cleared!", True, WHITE)
    score_level_cleared = bold_font2.render(str(score), True, WHITE)

    if level.number_of_birds >= 0 and len(pigs) == 0:
        if bonus_score_once:
            score += (level.number_of_birds - 1) * 10000
        bonus_score_once = False
        game_state = 4

        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(level_cleared, (450, 90))

        # Display star ratings based on the score
        if level.one_star <= score < level.two_star:
            screen.blit(star1, (310, 190))
        if level.two_star <= score < level.three_star:
            screen.blit(star2, (520, 190))
        if score >= level.three_star:
            screen.blit(star3, (730, 190))

def draw_level_failed():
    """Display the 'Level Failed' screen."""
    global game_state
    failed = bold_font3.render("Level Failed", True, WHITE)
    if level.number_of_birds <= 0 and time.time() - t2 > 5 and len(pigs) > 0:
        game_state = 3
        rect = pygame.Rect(300, 0, 600, 800)
        pygame.draw.rect(screen, BLACK, rect)
        screen.blit(failed, (450, 90))
        screen.blit(pig_happy, (380, 120))
        screen.blit(replay_button, (520, 460))

def restart():
    """Remove all objects from the level to restart."""
    global pigs, birds, columns, beams

    # Clear pigs
    pigs_to_remove = pigs.copy()
    for pig in pigs_to_remove:
        game_space.remove(pig)
    pigs.clear()

    # Clear birds
    birds_to_remove = birds.copy()
    for bird in birds_to_remove:
        game_space.remove(bird)
    birds.clear()

    # Clear columns
    columns_to_remove = columns.copy()
    for column in columns_to_remove:
        game_space.remove(column)
    columns.clear()

    # Clear beams
    beams_to_remove = beams.copy()
    for beam in beams_to_remove:
        game_space.remove(beam)
    beams.clear()

def post_solve_bird_pig(arbiter, space, _):
    """Handle collision between bird and pig."""
    global score
    surface = screen
    bird_body, pig_body = arbiter['bird'], arbiter['pig']
    p = to_pygame(bird_body['position'])
    p2 = to_pygame(pig_body['position'])
    r = 30
    pygame.draw.circle(surface, BLACK, p, r, 4)
    pygame.draw.circle(surface, RED, p2, r, 4)

    pigs_to_remove = []
    for pig in pigs:
        if pig_body == pig.body:
            pig.life -= 20
            if pig.life <= 0:
                pigs_to_remove.append(pig)
                score += 10000

    for pig in pigs_to_remove:
        game_space.remove(pig)
        pigs.remove(pig)

def post_solve_bird_wood(arbiter, space, _):
    """Handle collision between bird and wood."""
    global score
    poly_to_remove = []

    # Assuming arbiter['impulse'] is a vector representing the total impulse
    impulse_magnitude = (arbiter['impulse'][0]**2 + arbiter['impulse'][1]**2) ** 0.5
    if impulse_magnitude > 1100:
        bird_shape, wood_shape = arbiter['bird'], arbiter['wood']
        for column in columns:
            if wood_shape == column.shape:
                poly_to_remove.append(column)
        for beam in beams:
            if wood_shape == beam.shape:
                poly_to_remove.append(beam)

        for poly in poly_to_remove:
            if poly in columns:
                columns.remove(poly)
            if poly in beams:
                beams.remove(poly)
            game_space.remove(poly)
        
        score += 5000

def post_solve_pig_wood(arbiter, space, _):
    """Handle collision between pig and wood."""
    global score
    pigs_to_remove = []

    # Assuming arbiter['impulse'] is a vector representing the total impulse
    impulse_magnitude = (arbiter['impulse'][0]**2 + arbiter['impulse'][1]**2) ** 0.5
    if impulse_magnitude > 700:
        pig_shape, wood_shape = arbiter['pig'], arbiter['wood']
        for pig in pigs:
            if pig_shape == pig.shape:
                pig.life -= 20
                if pig.life <= 0:
                    pigs_to_remove.append(pig)
                    score += 10000

        for pig in pigs_to_remove:
            game_space.remove(pig)
            pigs.remove(pig)

# bird and pigs
collision_handlers = [
    {'type1': 'bird', 'type2': 'pig', 'handler': post_solve_bird_pig},
    {'type1': 'bird', 'type2': 'wood', 'handler': post_solve_bird_wood},
    {'type1': 'pig', 'type2': 'wood', 'handler': post_solve_pig_wood},
]

# Initialize Level
level = Level(game_space)
level.number = 0
level.load_level()

running = True
while running:
    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w:
                # Toggle wall
                if wall:
                    game_space = [obj for obj in game_space if obj != 'wall']
                    wall = False
                else:
                    create_static_floor(game_space)
                    wall = True
            elif event.key == pygame.K_s:
                # Space effect (e.g., low gravity)
                level.bool_space = True
            elif event.key == pygame.K_n:
                # Normal gravity
                level.bool_space = False
                game_space.gravity = (0.0, -700.0)

        if (pygame.mouse.get_pressed()[0] and 100 < x_mouse < 250 and 370 < y_mouse < 550):
            mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and mouse_pressed:
            # Release a new bird
            mouse_pressed = False
            if level.number_of_birds > 0:
                level.number_of_birds -= 1
                t1 = time.time() * 1000
                xo, yo = 154, 156

                # Create a new bird
                if mouse_distance > rope_length:
                    mouse_distance = rope_length
                bird = Bird(mouse_distance, angle, xo, yo, game_space) if x_mouse < sling_x + 5 else Bird(-mouse_distance, angle, xo, yo, game_space)
                birds.append(bird)

                if level.number_of_birds == 0:
                    t2 = time.time()

        # Pause/Resume/Restart handling
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if x_mouse < 60 and 90 < y_mouse < 155:
                game_state = 1
            if game_state == 1:
                if 500 < x_mouse and 200 < y_mouse < 300:
                    game_state = 0  # Resume
                elif 500 < x_mouse and 300 < y_mouse < 400:
                    restart()
                    level.load_level()
                    game_state = 0
                    bird_path = []
            if game_state == 3 and 500 < x_mouse < 620 and y_mouse > 450:
                restart()
                level.load_level()
                game_state = 0
                bird_path = []
                score = 0
            if game_state == 4 and x_mouse > 610 and y_mouse > 450:
                restart()
                level.number += 1
                game_state = 0
                level.load_level()
                score = 0
                bird_path = []

    # Update the game state, physics, and rendering here
    level.update()
    physics_manager.update()
    renderer.render(level.get_all_objects())

    # Cap the frame rate
    clock.tick(50)
    pygame.display.set_caption(f"fps: {clock.get_fps()}")

pygame.quit()
