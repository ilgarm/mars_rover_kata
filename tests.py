import unittest
import command
import direction
from grid import Grid
from location import Location
from rover import Rover


class CommandTest(unittest.TestCase):
    def test_commands_mapping(self):
        self.assertEquals(command.to_commands('flbr'), [command.F, command.L, command.B, command.R])


class DirectionTest(unittest.TestCase):
    def test_direction_index(self):
        self.assertEquals(direction.N.get_index(), 0)
        self.assertEquals(direction.W.get_index(), 3)

    def test_get_direction_by_index(self):
        self.assertEquals(direction.E, direction.get_direction_by_index(1))
        self.assertEquals(direction.S, direction.get_direction_by_index(2))


class GridTest(unittest.TestCase):
    def test_grid_dimension(self):
        grid = Grid(3, 3)
        self.assertEquals(grid.dimensionX, grid.dimensionY)
        self.assertEquals(grid.dimensionX, 3)

    def test_grid_has_obstacle(self):
        grid = Grid(3, 3)
        grid.place_obstacle(0, 1)

        self.assertTrue(grid.has_obstacle(0, 1))
        self.assertFalse(grid.has_obstacle(1, 1))

    def test_grid_representation(self):
        grid = Grid(3, 3)
        self.assertEquals(str(grid), 'ooo\nooo\nooo\n')

    def test_grid_representation_with_obstacles(self):
        grid = Grid(3, 3)
        grid.place_obstacle(0, 0)
        self.assertEquals(str(grid), 'xoo\nooo\nooo\n')

        grid.place_obstacle(1, 1)
        self.assertEquals(str(grid), 'xoo\noxo\nooo\n')


class LocationTest(unittest.TestCase):
    def assert_location(self, location1, location2):
        self.assertEquals(location1.position, location2.position)
        self.assertEquals(location1.direction, location2.direction)

    def test_next_location(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.N)

        next_location = location.next_location(command.F)
        self.assert_location(Location(grid, 0, 1, direction.N), next_location)

        next_location = next_location.next_location(command.R)
        self.assert_location(Location(grid, 0, 1, direction.E), next_location)

        next_location = next_location.next_location(command.F)
        self.assert_location(Location(grid, 1, 1, direction.E), next_location)

    def test_next_location_wrapped(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.W)

        next_location = location.next_location(command.F)
        self.assert_location(Location(grid, 2, 0, direction.W), next_location)

        next_location = next_location.next_location(command.L)
        self.assert_location(Location(grid, 2, 0, direction.S), next_location)

        next_location = next_location.next_location(command.F)
        self.assert_location(Location(grid, 2, 2, direction.S), next_location)

    def test_location_on_obstacle(self):
        grid = Grid(3, 3)
        grid.place_obstacle(0, 1)
        location = Location(grid, 0, 0, direction.N)

        self.assertFalse(location.is_on_obstacle())

        next_location = location.next_location(command.F)
        self.assertTrue(next_location.is_on_obstacle())


class RoverTest(unittest.TestCase):
    def assert_location(self, location, posX, posY, direction):
        self.assertEquals(location.position, (posX, posY))
        self.assertEquals(location.direction, direction)

    def test_rover_initial_position(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.N)
        rover = Rover(location)

        self.assert_location(rover.location, 0, 0, direction.N)

    def test_rover_can_move(self):
        grid = Grid(3, 3)
        location = Location(grid, 1, 1, direction.W)
        rover = Rover(location)

        rover.move(command.F)
        self.assert_location(rover.location, 0, 1, direction.W)

        rover.move(command.F)
        self.assert_location(rover.location, 2, 1, direction.W)

    def test_rover_can_turn(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.W)
        rover = Rover(location)

        rover.move(command.R)
        self.assert_location(rover.location, 0, 0, direction.N)

        rover.move(command.L)
        self.assert_location(rover.location, 0, 0, direction.W)

        rover.move(command.L)
        self.assert_location(rover.location, 0, 0, direction.S)

    def test_rover_can_move_and_turn(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.N)
        rover = Rover(location)

        rover.move(command.F)
        self.assert_location(rover.location, 0, 1, direction.N)

        rover.move(command.F)
        self.assert_location(rover.location, 0, 2, direction.N)

        rover.move(command.R)
        self.assert_location(rover.location, 0, 2, direction.E)

        rover.move(command.F)
        self.assert_location(rover.location, 1, 2, direction.E)

        rover.move(command.F)
        self.assert_location(rover.location, 2, 2, direction.E)

    def test_rover_can_move_and_turn_batch(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.N)
        rover = Rover(location)

        rover.move(command.to_commands('ffrff'))
        self.assert_location(rover.location, 2, 2, direction.E)

    def test_rover_can_wrap(self):
        grid = Grid(3, 3)
        location = Location(grid, 0, 0, direction.N)
        rover = Rover(location)

        rover.move(command.B)
        self.assert_location(rover.location, 0, 2, direction.N)

        rover.move(command.to_commands('lf'))
        self.assert_location(rover.location, 2, 2, direction.W)

    def test_rover_can_detect_obstacle(self):
        grid = Grid(3, 3)
        grid.place_obstacle(0, 2)

        location = Location(grid, 0, 0, direction.N)
        rover = Rover(location)

        rover.move(command.to_commands('fff'))
        self.assert_location(rover.location, 0, 1, direction.N)
        self.assertEquals(1, rover.last_moved_steps)
        self.assertTrue(rover.faced_obstacle)
