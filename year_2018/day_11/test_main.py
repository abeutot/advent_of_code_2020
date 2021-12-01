import sys
import itertools
from functools import lru_cache


@lru_cache(maxsize=None)
def power_level(x, y, serial):
    # print('xy:', x, y, serial)
    rack_id = x + 10
    power  = rack_id * y
    power += serial
    power *= rack_id
    power = power // 100 - (power // 1000 * 10)
    power -= 5
    return power


def test_power_level():
    assert power_level(3, 5, 8) == 4
    assert power_level(122, 79, 57) == -5
    assert power_level(217, 196, 39) == 0
    assert power_level(101, 153, 71) == 4

    assert [power_level(x, y, 18)
            for x, y in itertools.product(
                range(33, 33 + 3),
                range(45, 45 + 3),
            )] == [4, 3, 1, 4, 3, 2, 4, 4, 4]

    assert [power_level(x, y, 42)
            for x, y in itertools.product(
                range(21, 21 + 3),
                range(61, 61 + 3),
            )] == [4, 3, 3, 3, 3, 3, 3, 4, 4]


def largest_square(serial, size):
    top_x, top_y, power = None, None, -sys.maxsize

    for x, y in itertools.product(range(1, 301 - size + 1), range(1, 301 - size + 1)):
        # print('x,y:', x, y)
        p = sum(power_level(x + i, y + j, serial) for i, j in itertools.product(range(0, size), range(0, size)))
        if p > power:
            top_x, top_y, power = x, y, p

    return top_x, top_y, power


def greatest_square(serial):
    top_x, top_y, size, power = None, None, None, -sys.maxsize
    for s in range(1, 300):
        nx, ny, np = largest_square(serial, s)
        if np > power:
            top_x, top_y, size, power = nx, ny, s, np

    return top_x, top_y, size, power


def test_largest_square():
    assert largest_square(18, 3) == (33, 45, 29)
    assert largest_square(42, 3) == (21, 61, 30)

    assert largest_square(18, 16) == (90, 269, 113)
    assert largest_square(42, 12) == (232, 251, 119)


if __name__ == '__main__':
    print('largest_square:', largest_square(9435, 3))
    print('greatest_square:', greatest_square(9435))
