import pygame

class GameLoopService:
    def __init__(self, game_controller: object) -> None:
        self.game_controller = game_controller
        self.is_running = False
        self.clock = pygame.time.Clock()

    def start(self):
        self.is_running = True
        self.run()

    def run(self):
        while self.is_running:
            self.is_running = self.game_controller.handle_events()
            self.game_controller.update()
            self.game_controller.draw()
            self.clock.tick(60)
