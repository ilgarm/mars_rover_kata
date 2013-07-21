class Grid:
    def __init__(self, dimensionX, dimensionY):
        self.dimensionX = dimensionX
        self.dimensionY = dimensionY

        self.obstacles = []

    def place_obstacle(self, posX, posY):
        if not self.has_obstacle(posX, posY):
            self.obstacles.append((posX, posY))

    def has_obstacle(self, posX, posY):
        return (posX, posY) in self.obstacles

    def __repr__(self):
        string = ''
        for posX in range(self.dimensionX):
            string += ''.join([self.get_cell_representation(posX, posY) for posY in range(self.dimensionY)])
            string += '\n'
        return string

    def get_cell_representation(self, posX, posY):
        return 'x' if self.has_obstacle(posX, posY) else 'o'
