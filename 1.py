"""
https://adventofcode.com/2023/day/1
"""

import pytest

CALIBRATION_FILENAME = 'input2.txt'

NUMBER_MAPPING = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def _search_to_int(search_str):
    """Convert the search string (either a verbal number like 'one' or an actual number like '1') into an int."""
    if search_str in NUMBER_MAPPING:
        return NUMBER_MAPPING[search_str]
    else:
        return int(search_str)


def get_calibration_value(line):
    """get the calibration value from a muddled up string"""

    # build a dict where the key is the index within the calib str, and the value is the number (int) found.
    found_values = {}

    # build list of search strings
    search_items = [str(n) for n in range(1, 10)] + list(NUMBER_MAPPING.keys())

    for search in search_items:
        try:
           found_values[line.index(search)] = _search_to_int(search)
           found_values[line.rindex(search)] = _search_to_int(search)
        except ValueError:
            next

    numbers_in_order = [b for (a, b) in sorted(found_values.items())]
    return int('{}{}'.format(numbers_in_order[0], numbers_in_order[-1]))


@pytest.mark.parametrize(('input', 'expected'), [
    ['1abc2', 12], 
    ['pqr3stu8vwx', 38],
    ['a1b2c3d4e5f', 15],
    ['treb7uchet', 77]
])
def test_get_calibration_value_part_1(input, expected):
    assert get_calibration_value(input) == expected

@pytest.mark.parametrize(('input', 'expected'), [
    ['two1nine', 29], 
    ['eightwothree', 83],
    ['abcone2threexyz', 13],
    ['xtwone3four', 24],
    ['4nineeightseven2', 42],
    ['zoneight234', 14],
    ['7pqrstsixteen', 76]
])
def test_get_calibration_value_part_2(input, expected):
    assert get_calibration_value(input) == expected


def main(calibration_list):
    """Get the sum of all the calibration values"""
    return sum(get_calibration_value(calibration) for calibration in calibration_list)


def get_calibration_list_from_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    print(main(get_calibration_list_from_file(CALIBRATION_FILENAME)))
