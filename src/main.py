import pygame
from controllers import GameController
from services import GameLoopService

def main():
    pygame.init()
    game_controller = GameController()
    game_loop = GameLoopService(game_controller)
    game_loop.start()
    pygame.quit()

if __name__ == "__main__":
    main()
