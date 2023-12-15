"""
Advent of Code 2023 Day 15
"""

import re
import pytest

from collections import defaultdict, namedtuple


INPUT_FILE = 'input.txt'

Lens = namedtuple('Lens', ('label', 'focal_length'))


def get_hash_value_of_string(input):
    current_value = 0

    for c in input:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value

class InitializationSequence:

    ADD_OPERATION = '='
    REMOVE_OPERATION = '-'
    COMMAND_RE = re.compile(r'(?P<label>\w*)(?P<oper>[-=])(?P<focal>\d*)')

    def __init__(self):
        self.boxes = defaultdict(list)

    @staticmethod
    def parse_command(command):
        match = re.fullmatch(InitializationSequence.COMMAND_RE, command)
        return match.group('label'), match.group('oper'), int(match.group('focal')) if match.group('focal') else None

    def perform_sequence(self, commands):
        for command in commands:
            self.perform_step(command)

    def get_lens_from_box_by_label(self, box, label):
        """
        Retrieves a Lens object from a box [a list] by the lens' label. Also returns the index of the lens in the box.
        Does not modify the contents of the box.
        Returns None, None if nothing found.
        """
        for i, lens in enumerate(box):
            if lens.label == label:
                return lens, i

        return None, None

    def perform_step(self, command):
        label, operation, focal_length = self.parse_command(command)
        box_num = get_hash_value_of_string(label)
        box = self.boxes[box_num]

        if operation == InitializationSequence.ADD_OPERATION:
            lens = Lens(label=label, focal_length=focal_length)
            existing_lens, existing_loc = self.get_lens_from_box_by_label(box, label)
            if existing_lens is not None:
                # replace existing
                box[existing_loc] = lens
            else:
                # add lens to box
                box.append(lens)

        elif operation == InitializationSequence.REMOVE_OPERATION:
            existing_lens, existing_loc = self.get_lens_from_box_by_label(box, label)
            if existing_loc is not None:
                del box[existing_loc]

    def get_focusing_power(self):
        focusing_powers = []

        for box_num, box in self.boxes.items():
            for slot, lens in enumerate(box, start=1):
                focusing_powers.append( (box_num+1) * slot * lens.focal_length )

        return sum(focusing_powers)
        
    

@pytest.mark.parametrize(('input', 'expected'), [
    ('rn=1', ('rn', '=', '1')),
    ('cm-', ('cm', '-', None)),
    ('qp=3', ('qp', '=', '3')),
    ('cm=2', ('cm', '=', '2')),
    ('qp-', ('qp', '-', None)),
    ('pc=4', ('pc', '=', '4')),
    ('ot=9', ('ot', '=', '9')),
    ('ab=5', ('ab', '=', '5')),
    ('pc-', ('pc', '-', None)),
    ('pc=6', ('pc', '=', '6')),
    ('ot=7', ('ot', '=', '7')),
])
def test_parse_command(input, expected):
    assert InitializationSequence.parse_command(input) == expected

@pytest.mark.parametrize(('input', 'expected'), [
    ('HASH', 52),
    ('rn=1', 30),
    ('cm-', 253),
    ('qp=3', 97),
    ('cm=2', 47),
    ('qp-', 14),
    ('pc=4', 180),
    ('ot=9', 9),
    ('ab=5', 197),
    ('pc-', 48),
    ('pc=6', 214),
    ('ot=7', 231),
])
def test_get_hash_value_of_string(input, expected):
    assert get_hash_value_of_string(input) == expected

def get_input_from_file(filename):
    with open(filename, 'r') as f:
        return f.read().split(',')

def main():
    input = get_input_from_file(INPUT_FILE)
    
    init = InitializationSequence()
    init.perform_sequence(input)
    return init.get_focusing_power()

    # return sum(get_hash_value_of_string(s) for s in input)

if __name__=='__main__':
    print(main())
