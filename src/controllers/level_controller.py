import pygame
from models import Polygon, Pig, Bird


class Level:
    def __init__(self, space):
        self.pigs = []
        self.columns = []
        self.beams = []
        self.space = space
        self.number = 0
        self.number_of_birds = 4
        self.one_star = 30000
        self.two_star = 40000
        self.three_star = 60000
        self.bool_space = False

    def open_flat(self, x, y, n):
        """Create an open flat structure."""
        y0 = y
        for i in range(n):
            y = y0 + 100 + i * 100
            p = (x, y)
            self.columns.append(Polygon(p, 20, 85, self.space))  # Placeholder for dimensions
            p = (x + 60, y)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x + 30, y + 50)
            self.beams.append(Polygon(p, 85, 20, self.space))

    def closed_flat(self, x, y, n):
        """Create a closed flat structure."""
        y0 = y
        for i in range(n):
            y = y0 + 100 + i * 125
            p = (x + 1, y + 22)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x + 60, y + 22)
            self.columns.append(Polygon(p, 20, 85, self.space))
            p = (x + 30, y + 70)
            self.beams.append(Polygon(p, 85, 20, self.space))
            p = (x + 30, y - 30)
            self.beams.append(Polygon(p, 85, 20, self.space))

    def horizontal_pile(self, x, y, n):
        """Create a horizontal pile."""
        y += 70
        for i in range(n):
            p = (x, y + i * 20)
            self.beams.append(Polygon(p, 85, 20, self.space))

    def vertical_pile(self, x, y, n):
        """Create a vertical pile."""
        y += 10
        for i in range(n):
            p = (x, y + 85 + i * 85)
            self.columns.append(Polygon(p, 20, 85, self.space))

    def build_0(self):
        """Level 0 setup."""
        pig1 = Pig(900, 100, self.space)
        self.pigs.append(pig1)

        self.columns.append(Polygon((920, 120), 20, 85))
        self.beams.append(Polygon((900, 180), 85, 20))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_1(self):
        """Level 1 setup."""
        pig1 = Pig(800, 200, self.space)
        pig2 = Pig(1000, 250, self.space)
        self.pigs.append(pig1)
        self.pigs.append(pig2)

        self.columns.append(Polygon((820, 220), 20, 85))
        self.beams.append(Polygon((1000, 300), 85, 20))

        self.number_of_birds = 3
        if self.bool_space:
            self.number_of_birds = 6

    def build_2(self):
        """Level 2 setup."""
        pig1 = Pig(880, 180, self.space)
        self.pigs.append(pig1)
        pig2 = Pig(1000, 230, self.space)
        self.pigs.append(pig2)
        self.columns.append(Polygon((880, 80), 20, 85))
        self.beams.append(Polygon((880, 150), 85, 20))
        self.columns.append(Polygon((1000, 80), 20, 85))
        self.columns.append(Polygon((1000, 180), 20, 85))
        self.beams.append(Polygon((1000, 210), 85, 20))
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_3(self):
        """Level 3 setup."""
        pigs = [
            Pig(950, 320, self.space),
            Pig(885, 225, self.space),
            Pig(1005, 225, self.space)
        ]
        for pig in pigs:
            pig.life = 25
            self.pigs.append(pig)

        # Creating the structure
        positions = [
            (1100, 100), (1040, 100), (980, 100), (920, 100), (860, 100), (800, 100),
            (1070, 152), (950, 152), (1010, 180), (830, 152), (890, 180), (860, 223),
            (920, 223), (980, 223), (1040, 223), (890, 280), (1010, 280), (950, 300),
            (920, 350), (980, 350), (950, 400)
        ]
        for pos in positions:
            if pos[1] in [152, 180, 223, 280, 300, 400]:
                self.beams.append(Polygon(pos, 85, 20, self.space))
            else:
                self.columns.append(Polygon(pos, 20, 85, self.space))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_4(self):
        """Level 4 setup."""
        pigs = [
            Pig(900, 300, self.space),
            Pig(1000, 500, self.space),
            Pig(1100, 400, self.space)
        ]
        self.pigs.extend(pigs)
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_5(self):
        """Level 5 setup."""
        pigs = [
            Pig(900, 70, self.space),
            Pig(1000, 152, self.space)
        ]
        self.pigs.extend(pigs)

        for i in range(9):
            p = (800, 70 + i * 21)
            self.beams.append(Polygon(p, 85, 20, self.space))

        for i in range(4):
            # Add the remaining code for build_5 when more of the original file is reviewed
            pass

    def build_6(self):
        """Level 6 setup."""
        pig1 = Pig(920, 533, self.space)
        pig1.life = 40
        self.pigs.append(pig1)
        pig2 = Pig(820, 533, self.space)
        self.pigs.append(pig2)
        pig3 = Pig(720, 633, self.space)
        self.pigs.append(pig3)

        self.closed_flat(895, 423, 1)
        self.vertical_pile(900, 0, 5)
        self.vertical_pile(926, 0, 5)
        self.vertical_pile(950, 0, 5)
        
        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_7(self):
        """Level 7 setup."""
        pigs = [
            Pig(978, 180, self.space),
            Pig(978, 280, self.space),
            Pig(978, 80, self.space)
        ]
        for pig in pigs:
            pig.life = 30
            self.pigs.append(pig)

        self.open_flat(950, 0, 3)
        self.vertical_pile(850, 0, 3)
        self.vertical_pile(830, 0, 3)

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_8(self):
        """Level 8 setup."""
        pigs = [
            Pig(1000, 180, self.space),
            Pig(1078, 280, self.space),
            Pig(900, 80, self.space)
        ]
        for pig in pigs:
            pig.life = 30
            self.pigs.append(pig)

        self.open_flat(1050, 0, 3)
        self.open_flat(963, 0, 2)
        self.open_flat(880, 0, 1)

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_9(self):
        """Level 9 setup."""
        pigs = [
            Pig(1000, 180, self.space),
            Pig(900, 180, self.space)
        ]
        for pig in pigs:
            pig.life = 20
            self.pigs.append(pig)

        self.open_flat(1050, 0, 3)
        self.open_flat(963, 0, 2)
        self.open_flat(880, 0, 2)
        self.open_flat(790, 0, 3)

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_10(self):
        """Level 10 setup."""
        pigs = [
            Pig(960, 250, self.space),
            Pig(820, 160, self.space),
            Pig(1100, 160, self.space)
        ]
        for pig in pigs:
            pig.life = 20
            self.pigs.append(pig)

        self.vertical_pile(900, 0, 3)
        self.vertical_pile(930, 0, 3)
        self.vertical_pile(1000, 0, 3)
        self.vertical_pile(1030, 0, 3)
        self.horizontal_pile(970, 250, 2)
        self.horizontal_pile(820, 0, 4)
        self.horizontal_pile(1100, 0, 4)

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def build_11(self):
        """Level 11 setup."""
        pigs = [
            Pig(820, 177, self.space),
            Pig(960, 150, self.space),
            Pig(1100, 130, self.space),
            Pig(890, 270, self.space)
        ]
        pigs[-1].life = 30  # Set life for the last pig
        self.pigs.extend(pigs)

        self.horizontal_pile(800, 0, 5)
        self.horizontal_pile(950, 0, 3)
        self.horizontal_pile(1100, 0, 2)

        self.vertical_pile(745, 0, 2)
        self.vertical_pile(855, 0, 2)
        self.vertical_pile(900, 0, 2)
        self.vertical_pile(1000, 0, 2)

        p = (875, 230)
        self.beams.append(Polygon(p, 85, 20, self.space))

        self.number_of_birds = 4
        if self.bool_space:
            self.number_of_birds = 8

    def load_level(self):
        """Load the level based on the current level number."""
        try:
            build_name = f"build_{self.number}"
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = f"build_{self.number}"
            getattr(self, build_name)()
