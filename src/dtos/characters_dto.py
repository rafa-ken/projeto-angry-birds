class CharacterDTO:
    def __init__(self, name, health, speed, position):
        self.name = name
        self.health = health
        self.speed = speed
        self.position = position

    def to_dict(self):
        # Convert the DTO to a dictionary, useful for serializing or passing data around
        return {
            'name': self.name,
            'health': self.health,
            'speed': self.speed,
            'position': self.position,
        }

    @classmethod
    def from_model(cls, character_model):
        # Create a CharacterDTO from a CharacterModel instance
        return cls(
            name=character_model.name,
            health=character_model.health,
            speed=character_model.speed,
            position=character_model.polygon.position
        )
