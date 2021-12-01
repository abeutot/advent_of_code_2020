import sys
import itertools
from operator import itemgetter


input_test = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


def parse_coord(c):
    name, range_ = c.split('=')
    range_ = tuple(map(int, range_.split('..')))

    return (name, range_)


def parse(input_):
    return [tuple(map(
        itemgetter(1),
        sorted(map(parse_coord, pair.split(', ')), key=itemgetter(0)),
    )) for pair in input_.rstrip('\n').split('\n')]


def test_parse():
    assert parse(input_test) == [
        ((495,), (2, 7)),
        ((495, 501), (7,)),
        ((501,), (3, 7)),
        ((498,), (2, 4)),
        ((506,), (1, 2)),
        ((498,), (10, 13)),
        ((504,), (10, 13)),
        ((498, 504), (13,)),
    ]


def print_map(x, y, X, Y, clay, water, rest):
    print()
    for j in range(min(y, 0), Y):
        for i in range(x, X):
            pos = (i, j)

            e = '.'

            if pos in clay:
                e = '#'
            elif pos in water:
                e = '+' if j == 0 else '|'
            elif pos in rest:
                e = '~'

            print(e, end='')
        print()


def flow(coordinates):
    x, y = sys.maxsize, sys.maxsize
    X, Y = 0, 0
    clay = set()
    water = set()
    rest = set()

    for rx, ry in coordinates:
        for i in range(rx[0], rx[-1] + 1):
            for j in range(ry[0], ry[-1] + 1):
                x = min(x, i - 1)
                X = max(X, i + 2)
                y = min(y, j)
                Y = max(Y, j + 1)
                clay.add((i, j))

    new_water = {(500, 0)}
    for iteration in itertools.count(1):
        # print('iteration:', iteration)
        # print_map(x, y, X, Y, clay, water, rest)

        new_coord = list(new_water)
        new_water = set()

        # print('will look into:', new_coord)

        # flow existing water
        for wx, wy in new_coord:
            if wy + 1 >= Y:
                continue

            below = (wx, wy + 1)
            left = (wx - 1, wy)
            right = (wx + 1, wy)

            if below in clay or below in rest:
                # propagate on the sides
                if left not in clay and left not in water and left not in rest:
                    new_water.add(left)

                if right not in clay and right not in water and right not in rest:
                    new_water.add(right)

                continue

            # else below should be water or sand
            if below in water:
                continue

            new_water.add(below)

        # print('new_water:', new_water)
        if new_water:
            water |= new_water
            # try to flow the water as much as we can
            continue

        # if no new water, try to see if we have rest water candidates
        new_rest = set()
        # look for existing flow that would turn into rest
        for pos in list(water):
            if pos in rest or pos in new_rest:
                # already transformed
                continue

            wx, wy = pos

            left = None
            for i in itertools.count(wx - 1, -1):
                if (i, wy) in water:
                    continue
                if (i, wy) in clay:
                    left = i + 1
                    break
                break

            if left is None:
                continue

            right = None
            for i in itertools.count(wx + 1, 1):
                if (i, wy) in water:
                    continue
                if (i, wy) in clay:
                    right = i
                    break
                break

            if right is None:
                continue

            new_rest |= {(i, wy) for i in range(left, right)}

            # reevaluate previous water points
            new_water |= {(i, j) for i, j in water if left <= i < right and j == wy - 1}

        if not new_rest:
            break

        rest |= new_rest
        water -= new_rest

    return (
        len(rest),
        len(rest) + sum(1 for _, j in water if y <= j < Y),
    )


def test_flow():
    assert flow(parse(input_test)) == (29, 57)


if __name__ == '__main__':
    input_ = parse(open('input.txt').read())
    part2, part1 = flow(input_)
    print('part1:', part1)
    print('part2:', part2)
