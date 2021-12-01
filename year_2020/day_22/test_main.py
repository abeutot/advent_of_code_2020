import itertools
from operator import add
from functools import reduce


input_test = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


def parse(input_):
    p1, p2 = input_.rstrip('\n').split('\n\n')

    assert p1.startswith('Player 1:\n')
    assert p2.startswith('Player 2:\n')

    p1 = list(map(int, p1.split('\n')[1:]))
    p2 = list(map(int, p2.split('\n')[1:]))

    return p1, p2


def test_parse():
    assert parse(input_test) == (
        [9, 2, 6, 3, 1],
        [5, 8, 4, 7, 10],
    )


def round(decks):
    (t1, *p1), (t2, *p2) = decks

    if t1 > t2:
        winner = p1
    elif t2 > t1:
        winner = p2
    else:
        raise RuntimeError('Unsupported tie')

    winner.extend(reversed(sorted((t1, t2))))

    return (p1, p2)


def test_round():
    decks = parse(input_test)
    assert round(decks) == (
        [2, 6, 3, 1, 9, 5],
        [8, 4, 7, 10],
    )


def game(decks):
    p1, p2 = decks

    while p1 and p2:
        p1, p2 = round((p1, p2))

    winner = p1 if p1 else p2

    return reduce(
        add,
        (a * b for a, b in zip(reversed(winner), itertools.count(1))),
    )


def test_game():
    assert game(parse(input_test)) == 306


def game2(decks):
    p1, p2 = decks

    previous = set()

    while p1 and p2:
        config = hash(tuple(itertools.chain(p1, [-42], p2)))
        if config in previous:
            return True, p1

        previous.add(config)

        # print('p1:', p1)
        # print('p2:', p2)
        # print()

        (t1, *p1), (t2, *p2) = p1, p2

        if t1 <= len(p1) and t2 <= len(p2):
            winner, winner_deck = game2((p1[:t1], p2[:t2]))
            if winner:
                winner = p1
            else:
                winner = p2
        else:
            if t1 < t2:
                winner = p2
            elif t2 < t1:
                winner = p1
            else:
                raise RuntimeError('Unuspported tie')

        if winner is p1:
            p1.extend((t1, t2))
        else:
            p2.extend((t2, t1))

    if p1:
        return True, p1
    else:
        assert p2
        return False, p2


def part2(decks):
    _, winner_deck = game2(decks)
    return reduce(
        add,
        (a * b for a, b in zip(reversed(winner_deck), itertools.count(1))),
    )


def test_part2():
    assert part2(parse(input_test)) == 291


if __name__ == '__main__':
    decks = parse(open('input.txt').read())
    print('part1:', game(decks))
    print('part2:', part2(decks))
