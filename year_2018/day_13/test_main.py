import copy
import itertools


def parse(input_):
    tr = str.maketrans('><v^', '--||')

    map_ = {}
    carts = {}
    for y, l in enumerate(input_.split('\n')):
        for x, v in enumerate(l):
            k = (x, y)
            if v in ('><v^'):
                carts[k] = ('left', v)
                v = v.translate(tr)
            map_[k] = v

    return x + 1, y + 1, carts, map_


class Collision(Exception):
    def __init__(self, x, y):
        self.x, self.y = x, y


def move(X, Y, carts, map_, collision_handling=False):
    directions = {
        'right': {
            '^': '>',
            '>': 'v',
            'v': '<',
            '<': '^',
        },
        'left': {
            '^': '<',
            '<': 'v',
            'v': '>',
            '>': '^',
        },
        'straight': {
            '^': '^',
            '>': '>',
            'v': 'v',
            '<': '<',
        },
    }
    next_directions = {
        'left': 'straight',
        'straight': 'right',
        'right': 'left',
    }

    new_carts = {}
    active_positions = set(carts)  # we need to track current positions
    for (x, y), (next_turn, dir_) in sorted(carts.items(), key=lambda t: t[0][::-1]):
        if (x, y) not in active_positions:
            # it's been removed
            continue

        active_positions.remove((x, y))

        next_x, next_y = x, y

        if dir_ == '>':
            next_x += 1
        elif dir_ == '<':
            next_x -= 1
        elif dir_ == '^':
            next_y -= 1
        elif dir_ == 'v':
            next_y += 1

        if (next_x, next_y) in active_positions:

            if not collision_handling:
                raise Collision(next_x, next_y)

            # ignore other cart since it was crashed into
            active_positions.remove((next_x, next_y))
            new_carts.pop((next_x, next_y), None)
            continue

        next_track = map_[(next_x, next_y)]

        if next_track == '/':
            if dir_ in '^v':
                dir_ = directions['right'][dir_]
            elif dir_ in '><':
                dir_ = directions['left'][dir_]
        elif next_track == '\\':
            if dir_ in '^v':
                dir_ = directions['left'][dir_]
            elif dir_ in '><':
                dir_ = directions['right'][dir_]
        elif next_track == '+':
            dir_ = directions[next_turn][dir_]
            next_turn = next_directions[next_turn]
        elif next_track == '-':
            assert dir_ in '<>'
        elif next_track == '|':
            assert dir_ in '^v'
        else:
            raise RuntimeError('Unexpected next track: ' + next_track)

        active_positions.add((next_x, next_y))
        new_carts[(next_x, next_y)] = (next_turn, dir_)

    return new_carts


def find_collision(X, Y, carts, map_):
    while True:
        try:
            carts = move(X, Y, carts, map_)
        except Collision as e:
            return e.x, e.y


def print_map(X, Y, carts, map_):
    for y in range(Y):
        for x in range(X):
            k = (x, y)
            if k in carts:
                print(carts[k][1], end='')
                continue
            print(map_[k], end='')
        print('')



def find_last_cart(X, Y, carts, map_):
    while len(carts) > 1:
        carts = move(X, Y, carts, map_, True)

    return next(iter(carts))


def test_part1():
    X, Y, carts, map_ = parse("""/->--\\
|    ^
|    |
\\----/""")
    assert X == 6
    assert Y == 4
    assert carts == {
        (2, 0): ('left', '>'),
        (5, 1): ('left', '^'),
    }
    assert map_ == {
        (0, 0): '/',
        (0, 1): '|',
        (0, 2): '|',
        (0, 3): '\\',
        (1, 0): '-',
        (1, 1): ' ',
        (1, 2): ' ',
        (1, 3): '-',
        (2, 0): '-',
        (2, 1): ' ',
        (2, 2): ' ',
        (2, 3): '-',
        (3, 0): '-',
        (3, 1): ' ',
        (3, 2): ' ',
        (3, 3): '-',
        (4, 0): '-',
        (4, 1): ' ',
        (4, 2): ' ',
        (4, 3): '-',
        (5, 0): '\\',
        (5, 1): '|',
        (5, 2): '|',
        (5, 3): '/',
    }

    assert move(X, Y, carts, map_) == {
        (3, 0): ('left', '>'),
        (5, 0): ('left', '<'),
    }


def test_find_collision():
    stuff = parse(r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """)
    assert find_collision(*stuff) == (7, 3)


def test_find_last_cart():
    stuff = parse(r"""/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/""")
    assert find_last_cart(*stuff) == (6, 4)


if __name__ == '__main__':
    input_ = parse(open('input.txt').read().rstrip('\n'))
    print('part1:', find_collision(*input_))
    print('part2:', find_last_cart(*input_))
