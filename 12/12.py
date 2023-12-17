"""
Advent of Code 2023
Day 12
"""
import itertools

TEST_INPUT = 'test.txt'
REAL_INPUT = 'real.txt'

OPERATIONAL_SPRING = '.'
DAMAGED_SPRING = '#'


def get_num_arrangements(puzzle, success_conditions):
    found_solutions = []
    num_unknown = puzzle.count('?')
    filling_values = itertools.product([OPERATIONAL_SPRING, DAMAGED_SPRING], repeat=num_unknown)

    for possible_fill in filling_values:
        puzzle_solution = puzzle
        for fill_value in possible_fill:
            puzzle_solution = puzzle_solution.replace('?', fill_value, 1)

        if solution_meets_conditions(puzzle_solution, success_conditions):
            found_solutions.append(puzzle_solution)
        
    return len(found_solutions)

def solution_meets_conditions(solution, conditions):
    """
    Does the solution match the defined success conditions?
    e.g. #.#.# meets the conditions 1,1,1, but does not meet the conditions 2,3
    """
    return tuple(map(len, filter(None, solution.split('.')))) == conditions

def import_from_lines(lines):
    for line in lines:
        puzzle, raw_success_conditions = line.strip().split()
        success_conditions = tuple([int(cond) for cond in raw_success_conditions.split(',')])

        yield puzzle, success_conditions

def import_from_file(filename):
    with open(filename, 'r') as f:
        return import_from_lines(f.readlines())

def main():
    puzzles = import_from_file(REAL_INPUT)
    return sum(get_num_arrangements(puzzle, success_conditions) for puzzle, success_conditions in puzzles)

if __name__=='__main__':
    print(main())
