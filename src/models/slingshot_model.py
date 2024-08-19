import math

class SlingshotModel:
    __name__ = "Slingshot"

    def __init__(
            self,
            position: tuple,
            elasticity: float,
            max_pull_distance: int
        ) -> None:
        self.position = position
        self.elasticity = elasticity
        self.max_pull_distance = max_pull_distance
        self.loaded_bird = None

    def load_bird(self, bird):
        self.loaded_bird = bird

    def release_bird(self, angle, power):
        if self.loaded_bird:
            # Calculate velocity based on slingshot properties
            self.loaded_bird.velocity = [
                math.cos(math.radians(angle)) * power * self.elasticity,
                -math.sin(math.radians(angle)) * power * self.elasticity
            ]
            released_bird = self.loaded_bird
            self.loaded_bird = None
            return released_bird

    def __repr__(self) -> str:
        return f"Slingshot at {self.position} with elasticity {self.elasticity}"
