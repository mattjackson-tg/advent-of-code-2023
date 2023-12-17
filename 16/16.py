import itertools

from collections import namedtuple, defaultdict


TEST_GRID_FILE = 'test.txt'
REAL_GRID_FILE = 'real.txt'

EMPTY_TILE = '.'
VERTICAL_SPLIT_TILE = '|'
HORIZONTAL_SPLIT_TILE = '-'
MIRROR_BACK_TILE = '\\'
MIRROR_FORWARD_TILE = '/'

DIRECTION_UP = 'up'
DIRECTION_DOWN = 'down'
DIRECTION_LEFT = 'left'
DIRECTION_RIGHT = 'right'


REFLECTOR_TRANSLATIONS = {
    MIRROR_BACK_TILE: {
        DIRECTION_UP: DIRECTION_LEFT,
        DIRECTION_DOWN: DIRECTION_RIGHT,
        DIRECTION_RIGHT: DIRECTION_DOWN,
        DIRECTION_LEFT: DIRECTION_UP
    },
    MIRROR_FORWARD_TILE: {
        DIRECTION_UP: DIRECTION_RIGHT,
        DIRECTION_DOWN: DIRECTION_LEFT,
        DIRECTION_RIGHT: DIRECTION_UP,
        DIRECTION_LEFT: DIRECTION_DOWN
    }
}


Position = namedtuple('Position', ('x', 'y'))

class Tile:

    def __init__(self, grid, position, symbol):
        self.grid = grid
        self.position = position
        self.symbol = symbol
        self.energised = False
        self.direction_history = set()

    def reset_tile(self):
        self.energised = False
        self.direction_history = set()

    def __repr__(self):
        return "<Tile {}: {}>".format(self.position, self.symbol)

    def tile_above(self):
        return self.grid.get_tile((self.position.x, self.position.y-1))

    def tile_below(self):
        return self.grid.get_tile((self.position.x, self.position.y+1))

    def tile_right(self):
        return self.grid.get_tile((self.position.x+1, self.position.y))

    def tile_left(self):
        return self.grid.get_tile((self.position.x-1, self.position.y))


class Laser:

    def __init__(self, grid, start_position, start_direction):
        self.grid = grid
        self.position = start_position
        self.direction = start_direction

        tile = self.grid.get_tile(start_position)
        tile.energised = True
        self.direction, _ = self.get_new_direction_and_new_lasers(tile)

    @staticmethod
    def get_starting_lasers_for_laser(grid, laser_position, laser_direction):
        """A laser could immediately change direction or split upon being created. Use this method to go from a notional
        starting laser to a real set of starting lasers, with adjusted direction."""
        return []

    def next_tile(self):
        if self.direction == DIRECTION_UP:
            return self.grid.get_tile((self.position.x, self.position.y-1))
        elif self.direction == DIRECTION_DOWN:
            return self.grid.get_tile((self.position.x, self.position.y+1))
        elif self.direction == DIRECTION_LEFT:
            return self.grid.get_tile((self.position.x-1, self.position.y))
        elif self.direction == DIRECTION_RIGHT:
            return self.grid.get_tile((self.position.x+1, self.position.y))

    def can_continue(self):
        next_tile = self.next_tile()

        if next_tile and self.direction in next_tile.direction_history:
            return False

        return next_tile is not None

    def get_new_direction_and_new_lasers(self, new_tile):
        new_lasers = []
        new_direction = self.direction

        if new_tile.symbol == VERTICAL_SPLIT_TILE and self.direction in (DIRECTION_LEFT, DIRECTION_RIGHT):
            # follow laser upwards, return new laser going downward
            new_direction = DIRECTION_UP
            new_lasers.append(Laser(self.grid, self.position, DIRECTION_DOWN))
        elif new_tile.symbol == HORIZONTAL_SPLIT_TILE and self.direction in (DIRECTION_UP, DIRECTION_DOWN):
            # follow laser right, return new laser going leftward
            new_direction = DIRECTION_RIGHT
            new_lasers.append(Laser(self.grid, self.position, DIRECTION_LEFT))
        elif new_tile.symbol in (MIRROR_BACK_TILE, MIRROR_FORWARD_TILE):
            new_direction = REFLECTOR_TRANSLATIONS[new_tile.symbol][self.direction]

        return new_direction, new_lasers

    def progress(self):
        """
        Moves position of this laser, and returns any newly created lasers.
        Does not check if next tile is a valid continuation.
        """
        new_tile = self.next_tile()
        new_tile.direction_history.add(self.direction)

        self.position = new_tile.position
        new_tile.energised = True

        self.direction, new_lasers = self.get_new_direction_and_new_lasers(new_tile)

        return new_lasers


class Grid:
    
    def __init__(self, input_lines):
        self.grid = {}
        for y, line in enumerate(input_lines):
            for x, symbol in enumerate(line.strip()):
                pos = Position(x, y)
                self.grid[pos] = Tile(grid=self, position=pos, symbol=symbol)

    @property
    def tiles(self):
        tiles_by_row = defaultdict(list)
        for tile in self.grid.values():
            tiles_by_row[tile.position.y].append(tile)

        return [sorted(tiles, key=lambda tile: tile.position.x) for y, tiles in sorted(tiles_by_row.items(), key=lambda y_tiles: y_tiles[0])]


    def __repr__(self):
        return '\n'.join(''.join(tile.symbol for tile in tile_row) for tile_row in self.tiles)

    def energised_map(self):
        print('\n'.join(''.join('#' if tile.energised else '.' for tile in tile_row) for tile_row in self.tiles))

    def size(self):
        xs, ys = zip(*map(tuple, self.grid.keys()))
        return max(xs) + 1, max(ys) + 1
        

    def get_edge_tile_positions(self):
        size_x, size_y = self.size()
        return itertools.chain(
            (Position(0, y) for y in range(size_y)),  # left edge
            (Position(x, 0) for x in range(1, size_x)),  # top edge
            (Position(x, size_y-1) for x in range(1, size_x)), # bottom edge
            (Position(size_x-1, y) for y in range(1, size_y))  # right edge
        )


    def get_directions_from_edge(self, position):
        """Returns the direction that points from the edge. Only works for edge tiles. Returns two directions for corners."""
        size_x, size_y = self.size()
        directions = []

        if position.x == 0:  # left edge
            directions.append(DIRECTION_RIGHT)
        elif position.x == size_x - 1:  # right edge
            directions.append(DIRECTION_LEFT)

        if position.y == 0:  # top edge
            directions.append(DIRECTION_DOWN)
        elif position.y == size_y - 1:  # bottom edge
            directions.append(DIRECTION_UP)

        return directions

    def get_tile(self, position):
        return self.grid.get(position, None)

    def reset_all_tiles(self):
        for tile in self.grid.values():
            tile.reset_tile()

    def get_optimal_energised_tiles(self):
        energised = []

        for start_position in self.get_edge_tile_positions():
            for direction in self.get_directions_from_edge(start_position):
                self.reset_all_tiles()
                print("Starting from {}, going {}".format(start_position, direction))
                self.fire_laser(laser_start=start_position, start_direction=direction)
                energised.append(self.number_energised_tiles())
                print(energised)

        return max(energised)

    def fire_laser(self, laser_start=Position(x=0, y=0), start_direction=DIRECTION_RIGHT):
        lasers = [Laser(grid=self, start_position=laser_start, start_direction=start_direction)]
        while lasers:
            laser = lasers.pop()
            while laser.can_continue():
                lasers.extend(laser.progress())

    def number_energised_tiles(self):
        return sum(tile.energised for tile in self.grid.values())


def import_from_file(filename):
    with open(filename, 'r') as f:
        return Grid(f.readlines())


def main():
    grid = import_from_file(REAL_GRID_FILE)
    return grid.get_optimal_energised_tiles()

if __name__=='__main__':
    print(main())
