import itertools
from functools import reduce

import numpy as np


OPEN = 0
TREE = 1
LUMBERYARD = 2


def parse(input_):
    input_ = input_.rstrip('\n').translate(str.maketrans('.|#', '012'))
    area = [[int(x) for x in r] for r in input_.split('\n')]
    area = np.array(area)

    return area


def str_area(area):
    result = ''

    X, Y = area.shape

    for x in range(X):
        for y in range(Y):
            acre = area[x,y]
            if acre == OPEN:
                p = '.'
            elif acre == TREE:
                p = '|'
            elif acre == LUMBERYARD:
                p = '#'
            else:
                raise RuntimeError('inconsistent data')

            result += p
        result += '\n'

    return result


def evolution(area, minutes=10):
    X, Y = area.shape

    # add a margin to perform window sliding
    prev_area = np.zeros((X + 2, Y + 2), dtype=area.dtype)
    prev_area[1:-1,1:-1] = area
    area = np.array(prev_area)

    # keep a track of past computations
    past = {}

    for m in range(1, minutes + 1):
        prev_area, area = area, prev_area

        for x, y in itertools.product(range(1, X + 1), range(1, Y + 1)):
            # the window includes the current acre but it does not matter much
            # for the following conditions evaluations
            neighbors = prev_area[x - 1:x + 2, y - 1:y + 2]

            acre = prev_area[x, y]

            if acre == OPEN:
                if np.sum(neighbors == TREE) >= 3:
                    area[x,y] = TREE
                else:
                    area[x,y] = OPEN
                continue
            if acre == TREE:
                if np.sum(neighbors == LUMBERYARD) >= 3:
                    area[x,y] = LUMBERYARD
                else:
                    area[x,y] = TREE
                continue
            if acre == LUMBERYARD:
                if np.sum(neighbors == LUMBERYARD) >= 2 and np.sum(neighbors == TREE) >= 1:
                    area[x,y] = LUMBERYARD
                else:
                    area[x,y] = OPEN
                continue

        print('after %d minutes:' % m)
        str_ = str_area(area)
        print(str_)

        h = hash(str_)
        score = np.sum(area == LUMBERYARD) * np.sum(area == TREE)

        if h in past:
            past_m, past_score = past[h]

            cycle_len = m - past_m

            final_m = past_m + (minutes - past_m) % cycle_len

            for m, s in past.values():
                if m == final_m:
                    return s

        past[h] = (m, score)

    return score


def test_part1():
    input_test = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""
    assert evolution(parse(input_test)) == 1147

if __name__ == '__main__':
    input_ = parse(open('input.txt').read())
    print('part1:', evolution(input_))
    print('part2:', evolution(input_, 1000000000))
