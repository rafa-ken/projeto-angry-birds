import pygame
from models import CharacterModel, PolygonModel

class GameView:
    def __init__(self, screen):
        self.screen = screen

    def draw_character(self, character: CharacterModel):
        character.draw(self.screen)

    def draw_polygon(self, polygon: PolygonModel):
        polygon.draw(self.screen)

    def draw_background(self, color=(0, 0, 0)):
        self.screen.fill(color)

    def update_display(self):
        pygame.display.flip()
