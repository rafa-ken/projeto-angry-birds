from services import GameLoopService

class GameController:
    def __init__(self):
        self.game_loop_service = GameLoopService()

    def start_game(self):
        self.game_loop_service.run()

    def pause_game(self):
        self.game_loop_service.pause()

    def resume_game(self):
        self.game_loop_service.resume()

    def quit_game(self):
        self.game_loop_service.stop()
        self.cleanup()

    def cleanup(self):
        print("Cleaning up resources...")
