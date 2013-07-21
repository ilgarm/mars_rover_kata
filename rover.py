class Rover(object):
    def __init__(self, location):
        self.location = location
        self.last_moved_steps = 0
        self.faced_obstacle = False

    def move(self, commands):
        moves_counter = 0
        self.faced_obstacle = False

        if not hasattr(commands, '__iter__'):
            commands = (commands,)

        for command in commands:
            new_location = self.location.next_location(command)
            if new_location.is_on_obstacle():
                self.faced_obstacle = True
                break

            self.location = new_location
            moves_counter += 1

        self.last_moved_steps = moves_counter
