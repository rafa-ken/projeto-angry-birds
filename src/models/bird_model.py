class BirdModel:
    __name__ = "Bird"

    def __init__(
            self,
            name: str,
            weight: int,
            size: int,
            flying_speed: int,
            special_ability: str
        ) -> None:
        self.name = name
        self.weight = weight
        self.size = size
        self.flying_speed = flying_speed
        self.special_ability = special_ability

    def __repr__(self) -> str:
        return f"Bird {self.name}"
