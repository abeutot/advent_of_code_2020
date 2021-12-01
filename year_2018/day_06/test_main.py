import itertools
from pprint import pprint
from operator import itemgetter
from collections import defaultdict


def distance(x_a, y_a, x_b, y_b):
    return abs(x_b - x_a) + abs(y_b - y_a)


def largest_area_size(input_):
    input_ = [tuple(map(int, l.split(', ')))
              for l in input_.rstrip('\n').split('\n')]

    Y = max(map(itemgetter(0), input_))
    X = max(map(itemgetter(1), input_))

    areas = defaultdict(int)
    infinite_areas = set()

    for x in range(X + 1):
        for y in range(Y + 1):
            distances = [(i, distance(x, y, b, a))
                         for i, (a, b) in enumerate(input_)]

            i, min_ = min(distances, key=itemgetter(1))
            if sum(1 for a in map(itemgetter(1), distances) if a == min_) > 1:
                continue

            a = min(distances, key=itemgetter(1))[0]
            areas[a] += 1
            if x == 0 or y == 0 or x == X or y == Y:
                infinite_areas.add(a)

    pprint(areas)
    pprint({k: v for k, v in areas.items() if k not in infinite_areas})

    return max(v for a, v in areas.items() if a not in infinite_areas)


input_test = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
def test_min():
    assert largest_area_size(input_test) == 17


def closest_area_size(input_, max_distance):
    input_ = [tuple(map(int, l.split(', ')))
              for l in input_.rstrip('\n').split('\n')]

    Y = max(map(itemgetter(0), input_))
    X = max(map(itemgetter(1), input_))

    areas = defaultdict(int)
    infinite_areas = set()

    for x in range(X + 1):
        for y in range(Y + 1):
            distances = [(i, distance(x, y, b, a))
                         for i, (a, b) in enumerate(input_)]

            total_distances = sum(map(itemgetter(1), distances))

            if total_distances >= max_distance:
                continue

            areas[(x, y)] = 1

    return sum(areas.values())


def test_closest_area_size():
    assert closest_area_size(input_test, 32) == 16


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('largest area:', largest_area_size(input_))
    print('closest area:', closest_area_size(input_, 10000))
