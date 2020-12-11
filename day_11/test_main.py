from collections import defaultdict


def stable_seat(input_):
    seats = defaultdict(lambda: '.')
    for y, r in enumerate(input_.rstrip('\n').split('\n')):
        for x, s in enumerate(r):
            seats[(x, y)] = s
    Y = y + 1
    X = x + 1

    while True:
        # print('seats:', seats)
        new_seats = defaultdict(lambda: '.')

        for x in range(X):
            for y in range(Y):
                if seats[(x, y)] == '.':
                    continue

                adjacent = sum(1
                               for i in range(x - 1, x + 2)
                               for j in range(y - 1, y + 2)
                               if (i != x or j != y) and seats[(i, j)] == '#')
                new_seat = s = seats[(x, y)]
                if s == 'L' and adjacent == 0:
                    new_seat = '#'
                elif s == '#' and adjacent >= 4:
                    new_seat = 'L'
                new_seats[(x, y)] = new_seat

        # we can't directly compare the dicts since we test for out of bounds
        # access previously
        diff = [seats[(x, y)] == new_seats[(x, y)] for x in range(X) for y in range(Y)]
        if sum(diff) == len(diff):
            break

        seats = new_seats

    return sum(1 for s in seats.values() if s == '#')


def stable_seat_2(input_):
    seats = defaultdict(lambda: '.')
    for y, r in enumerate(input_.rstrip('\n').split('\n')):
        for x, s in enumerate(r):
            seats[(x, y)] = s
    Y = y + 1
    X = x + 1

    while True:
        # print('\n'.join(''.join(seats[(i, j)] for i in range(X)) for j in range(Y)))
        new_seats = defaultdict(lambda: '.')

        for x in range(X):
            for y in range(Y):
                if seats[(x, y)] == '.':
                    continue

                # top
                top = False
                for j in range(y - 1, -1, -1):
                    s = seats[(x, j)]
                    if s == '.':
                        continue
                    if seats[(x, j)] == '#':
                        top = True
                    break
                # bottom
                bottom = False
                for j in range(y + 1, Y):
                    s = seats[(x, j)]
                    if s == '.':
                        continue
                    if s == '#':
                        bottom = True
                    break
                # left
                left = False
                for i in range(x - 1, -1, -1):
                    s = seats[(i, y)]
                    if s == '.':
                        continue
                    if s == '#':
                        left = True
                    break
                # right
                right = False
                for i in range(x + 1, X):
                    s = seats[(i, y)]
                    if s == '.':
                        continue
                    if s == '#':
                        right = True
                    break
                # left top
                left_top = False
                for i, j in zip(range(x - 1, -1, -1), range(y - 1, -1, -1)):
                    s = seats[(i, j)]
                    if s == '.':
                        continue
                    if s == '#':
                        left_top = True
                    break
                # left bottom
                left_bottom = False
                for i, j in zip(range(x - 1, -1, -1), range(y + 1, Y)):
                    s = seats[(i, j)]
                    if s == '.':
                        continue
                    if s == '#':
                        left_bottom = True
                    break
                # right top
                right_top = False
                for i, j in zip(range(x + 1, X), range(y - 1, -1, -1)):
                    s = seats[(i, j)]
                    if s == '.':
                        continue
                    if s == '#':
                        right_top = True
                    break
                # right bottom
                right_bottom = False
                for i, j in zip(range(x + 1, X), range(y + 1, Y)):
                    s = seats[(i, j)]
                    if s == '.':
                        continue
                    if s == '#':
                        right_bottom = True
                    break
                adjacent = sum((top, bottom, left, right, left_top,
                                left_bottom, right_top, right_bottom))
                new_seat = s = seats[(x, y)]
                # print('x:', x, 'y:', y, 'adjacent:', adjacent, 'seats:', s, 't,b,l,r,lt,lb,rt,rb:', top, bottom, left, right, left_top, left_bottom, right_top, right_bottom)
                if s == 'L' and adjacent == 0:
                    new_seat = '#'
                elif s == '#' and adjacent >= 5:
                    new_seat = 'L'
                new_seats[(x, y)] = new_seat

        # we can't directly compare the dicts since we test for out of bounds
        # access previously
        diff = [seats[(x, y)] == new_seats[(x, y)] for x in range(X) for y in range(Y)]
        if sum(diff) == len(diff):
            break

        seats = new_seats

    return sum(1 for s in seats.values() if s == '#')


input_test = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
def test_stable_seat():
    assert stable_seat(input_test) == 37


def test_stable_seat_2():
    assert stable_seat_2(input_test) == 26


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('stable:', stable_seat(input_))
    print('stable 2:', stable_seat_2(input_))
