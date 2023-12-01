"""
https://adventofcode.com/2023/day/1
"""

import pytest

CALIBRATION_LIST = [
    ['1abc2', 12], 
    ['pqr3stu8vwx', 38],
    ['a1b2c3d4e5f', 15],
    ['treb7uchet', 77]
]


def get_calibration_value(line):
    """get the calibration value from a muddled up string"""
    values = [d for d in line if d.isdigit()]
    if not values:
        raise Exception("No values in string")

    return int("{}{}".format(values[0], values[-1]))


@pytest.mark.parametrize(('input', 'expected'), CALIBRATION_LIST)
def test_get_calibration_value(input, expected):
    assert get_calibration_value(input) == expected


def main():
    """Get the sum of all the calibration values"""
    return sum(get_calibration_value(calibration) for calibration, _ in CALIBRATION_LIST)


if __name__ == '__main__':
    print(main())
