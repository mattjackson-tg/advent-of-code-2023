"""
Identify symmetry in a map

Pseudocode explanation:
1. identify any consecutive rows in the input which are identical
2. For each consecutive identical row, hypothesise this is the symmetry point and do a brute-force test
3. Either symmetry will be found or it must exist vertically. If so, transpose whole input and start from the top (noting transposition for output)

Be careful of shadowing in-built `map` fn in this file.
"""

import pytest

TEST_INPUT = 'test.txt'
REAL_INPUT = 'map.txt'

SMUDGE_TOLERANCE = 1


def import_maps(input_text):
    maps = []
    map_ = []

    for line in map(lambda in_txt: in_txt.strip(), input_text):
        if line:
            map_.append(list(line))
        else:
            maps.append(map_)
            map_ = []

    # check for EOF without newline
    if map_:
        maps.append(map_)

    return maps

def get_reflection_errors(line1, line2):
    num_errors = sum(c1 != c2 for c1, c2 in zip(line1, line2))
    return num_errors

def is_map_symmetrical_at_row(map_, row_num):
    """
    For a map to be symmetrical at the row, concentric groups of lines outward must be equal, until we reach
    vertical bounds of map.
    So, if symmetrical at row 3 (between lines 3&4), lines 3 & 4 are equal, lines 2 & 5 are equal, 1 & 6, 0 & 7.
    Stop comparing after lower line hits zero, or upper line hits total number of lines-1 ( -1  due to 0-indexing).

    row_num should be zero-indexed.
    """
    line_comparisons = zip(range(row_num, -1, -1), range(row_num+1, len(map_)))
    reflection_errors = [get_reflection_errors(map_[line_a], map_[line_b]) for line_a, line_b in line_comparisons]
    return sum(reflection_errors) == SMUDGE_TOLERANCE
    
def transpose_map(map_):
    """rotate entire map counter-clockwise. This makes the first row now the first column."""
    return list(zip(*map_))

def find_horizontal_symmetry(map_):
    """Check each reflection point for symmetry"""
    for reflection_point in range(len(map_)-1):
        if is_map_symmetrical_at_row(map_, reflection_point):
            return reflection_point + 1  # (1-indexed)

    # no symmetry found
    return None

def find_symmetry(map):
    vertical_symmetry_point = None
    horizontal_symmetry_point = find_horizontal_symmetry(map)

    if horizontal_symmetry_point is None:
        vertical_symmetry_point = find_horizontal_symmetry(transpose_map(map))

    return ((horizontal_symmetry_point or 0) * 100) + (vertical_symmetry_point or 0)

def import_maps_from_file(input_file):
    with open(input_file, 'r') as f:
        return import_maps(f.readlines())


def main():
    maps = import_maps_from_file(REAL_INPUT)
    return sum(find_symmetry(map) for map in maps)


if __name__=='__main__':
    print(main())
