"""
Advent of Code 2023 Day 14

Part 1: two problems:
    1. compute what happens to layout when all rocks are rolled north
    2. compute load on north supports for given layout
"""

import itertools
from collections import defaultdict

TEST_LAYOUT = 'test.txt'
REAL_LAYOUT = 'layout.txt'

ROCK_SYMBOL = 'O'
CUBE_SYMBOL = '#'
SPACE_SYMBOL = '.'

NUM_CYCLES = 1000000000


class SpaceLayoutItem:
    is_blocking = False
    contributes_to_load = False
    symbol = SPACE_SYMBOL

    def __init__(self, layout, x, y):
        self.layout = layout
        self.x = x
        self.y = y

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    def can_move_up(self):
        return False

    def can_move_down(self):
        return False

    def can_move_left(self):
        return False

    def can_move_right(self):
        return False

class RockLayoutItem(SpaceLayoutItem):
    is_blocking = True
    contributes_to_load = True
    symbol = ROCK_SYMBOL

    def can_move_up(self):
        block_above = self.layout.get_item_at_position(self.x, self.y-1)
        return block_above.is_blocking is False

    def can_move_down(self):
        block_below = self.layout.get_item_at_position(self.x, self.y+1)
        return block_below.is_blocking is False

    def can_move_left(self):
        block_left = self.layout.get_item_at_position(self.x-1, self.y)
        return block_left.is_blocking is False

    def can_move_right(self):
        block_right = self.layout.get_item_at_position(self.x+1, self.y)
        return block_right.is_blocking is False

    def move_up(self):
        """this function does not check if the position up is blocking. caller should check."""
        self.layout.place_item_in_position(self, self.x, self.y-1)

    def move_down(self):
        self.layout.place_item_in_position(self, self.x, self.y+1)

    def move_left(self):
        self.layout.place_item_in_position(self, self.x-1, self.y)

    def move_right(self):
        self.layout.place_item_in_position(self, self.x+1, self.y)

class CubeLayoutItem(SpaceLayoutItem):
    is_blocking = True
    contributes_to_load = False
    symbol = CUBE_SYMBOL

class RockLayout:
    def __init__(self, text_layout):
        self.grid = {}

        for y, line in enumerate(text_layout):
            for x, character in enumerate(c for c in line if c.isprintable()):
                layout_item = self.get_layout_class(character)(self, x, y)
                self.grid[(x, y)] = layout_item

    def __repr__(self):
        return '\n'.join(''.join(map(repr, row)) for row in self.items)

    def serialize(self):
        return [''.join(map(repr, row)) for row in self.items]

    @property
    def items(self):
        cells_by_row = defaultdict(list)
        for ((x, y), item) in sorted(self.grid.items(), key=lambda loc_item: loc_item[0]):
            cells_by_row[y].append(item)

        return [items for y, items in sorted(cells_by_row.items(), key=lambda y_items: y_items[0])]


    def get_item_at_position(self, x, y):
        """Get the block in a given position, or (if it does not exist) return a blocking object that is in that position."""
        return self.grid.get((x, y), CubeLayoutItem(self, x, y))

    def place_item_in_position(self, item, x, y):
        """
        place the specified item into the specified new position, and fill the old position with a space.
        this method does not check that the space being moved in to is non-blocking. the caller should do that first.
        """
        old_position = (item.x, item.y)
        self.grid[(x, y)] = item
        item.x = x
        item.y = y

        self.grid[old_position] = SpaceLayoutItem(self, *old_position)

    def tilt_north(self):
        for item_row in self.items:
            for item in item_row:
                while item.can_move_up():
                    item.move_up()

    def tilt_south(self):
        for item_row in reversed(self.items):
            for item in item_row:
                while item.can_move_down():
                    item.move_down()

    def tilt_east(self):
        for item_row in self.items:
            for item in reversed(item_row):
                while item.can_move_right():
                    item.move_right()

    def tilt_west(self):
        for item_row in self.items:
            for item in item_row:
                while item.can_move_left():
                    item.move_left()

    def spin_cycle(self):
        previous_runs = []

        for n in range(NUM_CYCLES): 

            self.tilt_north()
            self.tilt_west()
            self.tilt_south()
            self.tilt_east()

            state = self.serialize()
            if state in previous_runs:
                # found cycle - compute all the way up to NUM_CYCLES
                cycle_length = len(previous_runs) - previous_runs.index(state)
                cycle_pos = (NUM_CYCLES - len(previous_runs)) % cycle_length
                final_position = previous_runs[-cycle_length:][cycle_pos-1]
                return RockLayout(final_position).calculate_north_supports_load()

            previous_runs.append(state)

    def calculate_north_supports_load(self):
        num_rows = len(self.items)
        total_load = 0
        for i, row in enumerate(self.items, start=0):
            total_load += sum(num_rows-i for rock in row if rock.contributes_to_load)
        
        return total_load

    def get_layout_class(self, character):
        return {
            ROCK_SYMBOL: RockLayoutItem,
            CUBE_SYMBOL: CubeLayoutItem,
            SPACE_SYMBOL: SpaceLayoutItem
        }[character]

def import_layout_from_file(filename):
    with open(filename, 'r') as f:
        return RockLayout(f.readlines()) 

def main():
    layout = import_layout_from_file(REAL_LAYOUT)
    return layout.spin_cycle()
    #return layout.calculate_north_supports_load()


if __name__=='__main__':
    print(main())
