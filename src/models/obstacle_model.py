class ObstacleModel:
    __name__ = "Obstacle"

    def __init__(
            self,
            position: tuple,
            size: tuple,
            durability: int
        ) -> None:
        self.position = position
        self.size = size
        self.durability = durability

    def take_damage(self, damage: int):
        self.durability -= damage
        if self.durability <= 0:
            self.durability = 0
            self.destroy()

    def destroy(self):
        # Placeholder for what happens when the obstacle is destroyed
        print(f"Obstacle at {self.position} destroyed!")

    def __repr__(self) -> str:
        return f"Obstacle at {self.position} with durability {self.durability}"
