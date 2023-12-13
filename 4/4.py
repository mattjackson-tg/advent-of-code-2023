TEST_INPUT = 'test.txt'
REAL_INPUT = 'cards.txt'


def get_point_value(card, winners):
    num_winners = sum(card_number in winners for card_number in card)
    return 2**(num_winners-1) if num_winners else 0

def import_draw_and_winners(input_line):
    draw = []
    winners = []

    _, raw_draw_and_winners = input_line.split(':')
    raw_draw, raw_winners = raw_draw_and_winners.split('|')
    draw = [int(raw_draw_num) for raw_draw_num in raw_draw.split()]
    winners = [int(raw_winner) for raw_winner in raw_winners.split()]

    return draw, winners

def import_from_lines(input_lines):
    return [import_draw_and_winners(input_line) for input_line in input_lines]

def import_from_file(filename):
    with open(filename, 'r') as input_file:
        return import_from_lines(input_file.readlines())

def main():
    winners_and_cards = import_from_file(REAL_INPUT)
    return sum([get_point_value(cards, winners) for winners, cards in winners_and_cards])

if __name__=='__main__':
    print(main())
