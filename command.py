class Command(object):
    def __init__(self, command, is_movement, is_rotation, factor):
        self.command = command
        self.is_movement = is_movement
        self.is_rotation = is_rotation
        self.factor = factor


F = Command('f', True, False, 1)
B = Command('b', True, False, -1)
L = Command('l', False, True, -1)
R = Command('R', False, True, 1)

commands = {
    'f': F,
    'b': B,
    'l': L,
    'r': R,
}


def to_commands(commands_string):
    return [commands[command] for command in commands_string]
