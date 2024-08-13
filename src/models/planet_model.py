class PlanetModel:
    __name__ = "Planet"

    def __init__(
            self,
            name: str,
            height: int,
            weight: int,
            diameter: int,
            distance_from_sun: int,
            distance_from_earth: int
        ) -> None:
        self.name = name
        self.height = height
        self.weight = weight
        self.diameter = diameter
        self.distance_from_sun = distance_from_sun
        self.distance_from_earth = distance_from_earth

    def __repr__(self) -> str:
        return f"Planet {self.name}"