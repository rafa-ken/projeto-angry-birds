class PolygonDTO:
    def __init__(self, vertices, position, color):
        self.vertices = vertices
        self.position = position
        self.color = color

    def to_dict(self):
        # Convert the DTO to a dictionary
        return {
            'vertices': self.vertices,
            'position': self.position,
            'color': self.color,
        }

    @classmethod
    def from_model(cls, polygon_model):
        # Create a PolygonDTO from a PolygonModel instance
        return cls(
            vertices=polygon_model.vertices,
            position=polygon_model.position,
            color=polygon_model.color
        )
