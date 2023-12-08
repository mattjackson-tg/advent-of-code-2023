from collections import defaultdict

import pytest

INPUT_FILE = 'input.txt'


BLUE = 'blue'
RED = 'red'
GREEN = 'green'

TEST_GAMES = {
    1: [{BLUE: 3, RED: 4, GREEN: 0}, {RED: 1, GREEN: 2, BLUE: 6}, {GREEN: 2, RED: 0, BLUE: 0}],
    2: [{BLUE: 1, GREEN: 2, RED: 0}, {GREEN: 3, BLUE: 4, RED: 1}, {GREEN: 1, BLUE: 1, RED: 0}],
    3: [{GREEN: 8, BLUE: 6, RED: 20}, {BLUE: 5, RED: 4, GREEN: 12}, {GREEN: 5, RED: 1, BLUE: 0}],
    4: [{GREEN: 1, RED: 3, BLUE: 6}, {GREEN: 3, RED: 6, BLUE: 0}, {GREEN: 3, BLUE: 15, RED: 14}],
    5: [{RED: 6, BLUE: 1, GREEN: 3}, {BLUE: 2, RED: 1, GREEN: 2}]
}

def is_draw_possible(draw, bag_contents):
    return all(draw[colour] <= bag_contents[colour] for colour in (RED, BLUE, GREEN))

def is_game_possible(game, bag_contents):
    return all(is_draw_possible(draw, bag_contents) for draw in game)

@pytest.mark.parametrize(('game', 'possible'), [
    [TEST_GAMES[1], True],
    [TEST_GAMES[2], True],
    [TEST_GAMES[3], False],
    [TEST_GAMES[4], False],
    [TEST_GAMES[5], True]
])
def test_is_game_possible(game, possible):
    bag = {RED: 12, GREEN: 13, BLUE: 14}
    assert is_game_possible(game, bag) is possible
    
def sum_possible_games(games, bag):
    return sum([(game_num if is_game_possible(game, bag) else 0) for game_num, game in games.items()])

def _parse_draw(draw_text):
    
    # small function to return the int contents of a string containing digits and letters
    _extract_number = lambda s: int(''.join(c for c in s if c.isdigit()))

    draw = {BLUE: 0, GREEN: 0, RED: 0}
    dice_count_text = draw_text.split(',')
    for dice_count in dice_count_text:
        for colour in (RED, BLUE, GREEN):
            if colour in dice_count:
                draw[colour] = _extract_number(dice_count)

    return draw

def parse_game(line):
    game_spec, game = line.split(':')
    game_number = game_spec.split()[1]
    draws_text = game.split(';')
    draws = [_parse_draw(draw_text) for draw_text in draws_text]

    return int(game_number), draws

def main(games):
    return sum_possible_games(games, {RED: 12, GREEN: 13, BLUE: 14})

if __name__ == '__main__':
    with open(INPUT_FILE, 'r') as f:
        games = {game_num: game for game_num, game in [parse_game(l) for l in f.readlines()]}

    print(main(games))
