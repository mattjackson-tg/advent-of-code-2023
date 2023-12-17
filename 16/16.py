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

    def get_tile(self, position):
        return self.grid.get(position, None)

    def fire_laser(self, laser_start=Position(x=0, y=0)):
        lasers = [Laser(grid=self, start_position=laser_start, start_direction=DIRECTION_RIGHT)]
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
    grid.fire_laser()
    import pdb; pdb.set_trace()
    return grid.number_energised_tiles()

if __name__=='__main__':
    print(main())
