import direction


class Location(object):
    def __init__(self, grid, posX, posY, direction):
        self.grid = grid
        self.position = (posX, posY)
        self.direction = direction

    def next_location(self, cmd):
        posX, posY = self.position
        dir = self.direction
        if cmd.is_movement:
            diffX, diffY = self.direction.get_step()
            posX = (posX + diffX) * cmd.factor
            posY = (posY + diffY) * cmd.factor
        else:
            current_index = self.direction.get_index()
            dir = direction.get_direction_by_index(current_index + cmd.factor)

        posX, posY = self.wrap_around_grid(posX, posY)
        return Location(self.grid, posX, posY, dir)

    def wrap_around_grid(self, posX, posY):
        def adjust_position(pos, dimension):
            return pos % dimension if pos >= 0 else dimension - pos % dimension + 1

        posX = adjust_position(posX, self.grid.dimensionX)
        posY = adjust_position(posY, self.grid.dimensionY)

        return posX, posY

    def is_on_obstacle(self):
        posX, posY = self.position
        return self.grid.has_obstacle(posX, posY)
