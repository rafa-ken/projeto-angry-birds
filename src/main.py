import pygame
from controllers import GameController, SlingshotController
from services import GameLoopService

def main():
    pygame.init()
    slingshot_controller = SlingshotController()
    game_controller = GameController()
    game_loop = GameLoopService(game_controller)
    game_loop.start()
    pygame.quit()

if __name__ == "__main__":
    main()
