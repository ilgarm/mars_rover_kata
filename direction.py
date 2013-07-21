class Direction(object):
    def __init__(self, cardinal, stepX, stepY):
        self.cardinal = cardinal
        self.stepX = stepX
        self.stepY = stepY

    def get_step(self):
        return self.stepX, self.stepY

    def get_index(self):
        return compass_rose.index(self.cardinal)


N = Direction('N', 0, 1)
E = Direction('E', 1, 0)
S = Direction('S', 0, -1)
W = Direction('W', -1, 0)

compass_rose = 'NESW'
directions = {
    'N': N,
    'E': E,
    'S': S,
    'W': W,
}


def get_direction_by_index(index):
    return directions[compass_rose[index % len(compass_rose)]]
