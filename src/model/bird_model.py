

class BirdModel:
    __name__ = "FckngBird"
    
    weight: str = None
    height: str = None
    color: str = None
    species: str = None
    age: str = None
    wingspan: str = None


    def __repr__(self, name):
        return f"{self.__name__} {name}"
