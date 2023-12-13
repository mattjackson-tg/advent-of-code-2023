import itertools
import pytest

TEST_SCHEMATIC_FILE = 'test.txt'
SCHEMATIC_FILE = 'schematic.txt'

class SchematicCell(object):
    SAMPLE_SYMBOL_VALUE = '$'
    EMPTY_VALUE = '.'

    def __init__(self, schematic, x, y, contents):
        self.schematic = schematic
        self.x = self.x_start = self.x_end = x
        self.y = y
        self.contents = contents

    def __repr__(self):
        return "<Cell: ({}, {}), '{}'>".format(
            self.x, self.y, self.contents
        )

    def coverage_cells(self):
        """All the cells this thing covers"""
        return [(x, self.y) for x in range(self.x_start, self.x_end+1)]

    def adjacent_cells(self):
        y_range = [self.y-1, self.y, self.y+1]
        x_range = [self.x_start-1] + [x for x in range(self.x_start, self.x_end+1)] + [self.x_end+1]
        cell_positions = [cell_pos for cell_pos in itertools.product(x_range, y_range) if cell_pos not in self.coverage_cells()]
        return [self.schematic.get_cell(*cell_pos) for cell_pos in cell_positions]

    def is_symbol(self):
        return not self.contents == self.EMPTY_VALUE

    def is_part_number(self):
        return False

    def is_gear(self):
        return self.contents == '*'

    def get_adjacent_part_numbers(self):
        adjacent_part_numbers = [cell for cell in self.adjacent_cells() if cell.contents.isdigit()]

        # uniquify then return values
        return [cell.contents for cell in list(set(adjacent_part_numbers))]

class SchematicPartNumberCell(SchematicCell):
    
    def __init__(self, schematic, x_start, x_end, y, contents):
        self.schematic = schematic
        self.x_start = x_start
        self.x_end = x_end
        self.y = y
        self.contents = contents

    def __repr__(self):
        return "<PartNumberCell: ({}-{}, {}), '{}'>".format(
            self.x_start, self.x_end, self.y, self.contents
        )

    def is_symbol(self):
        return False

    def is_part_number(self):
        return any(adjc.is_symbol() for adjc in self.adjacent_cells())

    def is_gear(self):
        return False
            

class Schematic(object):

    def __init__(self, values):
        """Create schematic. values is a 2D array of contained items in schematic"""
        self.cells = [self._parse_line(line, line_num) for line_num, line in enumerate(values)]
        self.grid = {}

        for line in self.cells: 
            for cell in line:
                for x in range(cell.x_start, cell.x_end+1):
                    self.grid[(x, cell.y)] = cell

    def __repr__(self):
        return repr(self.cells)

    def _parse_line(self, line, line_num):
        parsed_line = []
        found_number = ''

        for i, char in enumerate(line):
            if char.isdigit():
                found_number += char
            else:
                if found_number:
                    parsed_line.append(SchematicPartNumberCell(
                        self, x_start=i-len(found_number), x_end=i-1, y=line_num, contents=found_number
                    ))
                    found_number = ''
                parsed_line.append(SchematicCell(self, x=i, y=line_num, contents=char))

        if found_number:  # if the number is the last thing on the line, check again
            parsed_line.append(SchematicPartNumberCell(
                self, x_start=i-len(found_number)+1, x_end=i, y=line_num, contents=found_number
            ))


        return parsed_line

    def get_cell(self, x, y):
        try:
            return self.grid[(x, y)]
        except KeyError:
            return SchematicCell(self, x, y, SchematicCell.EMPTY_VALUE)

    def get_all_part_numbers(self):
        return [int(cell.contents) for cell in itertools.chain(*self.cells) if cell.is_part_number()]

    def get_all_gear_ratios(self):
        adjacent_parts_to_gears = [cell.get_adjacent_part_numbers() for cell in itertools.chain(*self.cells) if cell.is_gear()]
        return [int(parts[0]) * int(parts[1]) for parts in adjacent_parts_to_gears if len(parts) == 2]


def import_schematic_from_file(filename):
    with open(filename) as f:
        return import_schematic(f.readlines())

def import_schematic(lines):
    return Schematic([[c for c in line if c.isprintable()] for line in lines])

def main():
    schematic = import_schematic_from_file(SCHEMATIC_FILE)
    # print(sum(schematic.get_all_part_numbers()))
    print(sum(schematic.get_all_gear_ratios()))

if __name__=='__main__':
    main()


def test_import_schematic():
    TEST_SCHEMATIC = """
      12...7$.50...
      *..?.......12
      .4+==........""".strip().replace(" ", "")

    schematic = import_schematic(TEST_SCHEMATIC.splitlines())

    assert len(schematic.cells) == 3  # 3 lines
    assert len(schematic.cells[0]) == 11
    assert len(schematic.cells[1]) == 12
    assert len(schematic.cells[2]) == 13

    assert schematic.cells[0][0].contents == '12'
    assert schematic.cells[0][0].x_start == 0
    assert schematic.cells[0][0].x_end == 1
    assert schematic.cells[0][0].y == 0
    assert schematic.cells[0][0].is_symbol() is False

    assert schematic.cells[0][1].contents == '.'
    assert schematic.cells[0][1].x_start == 2
    assert schematic.cells[0][1].x_end == 2
    assert schematic.cells[0][1].y == 0
    assert schematic.cells[0][1].is_symbol() is False

    assert schematic.cells[0][-1].contents == '.'
    assert schematic.cells[0][-1].x_start == 12
    assert schematic.cells[0][-1].x_end == 12
    assert schematic.cells[0][-1].y == 0
    assert schematic.cells[0][-1].is_symbol() is False

    assert schematic.cells[1][0].contents == '*'
    assert schematic.cells[1][0].x_start == 0
    assert schematic.cells[1][0].x_end == 0
    assert schematic.cells[1][0].y == 1
    assert schematic.cells[1][0].is_symbol() is True

    assert schematic.cells[1][-2].contents == '.'
    assert schematic.cells[1][-2].x_start == 10
    assert schematic.cells[1][-2].x_end == 10
    assert schematic.cells[1][-2].y == 1
    assert schematic.cells[1][-2].is_symbol() is False

    assert schematic.cells[1][-1].contents == '12'
    assert schematic.cells[1][-1].x_start == 11
    assert schematic.cells[1][-1].x_end == 12
    assert schematic.cells[1][-1].y == 1
    assert schematic.cells[1][-1].is_symbol() is False


