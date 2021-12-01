import operator
import itertools

import numpy as np


def parse_cube(input_):
    input_ = input_.rstrip('\n')
    square = [[i == '#' for i in r] for r in input_.split('\n')]
    return np.array([square], dtype='bool')


def add_dim(a):
    new_a = np.zeros((1,) + a.shape, dtype='bool')
    new_a[0,] = a
    return new_a


def cycle(cube, cycle_count):
    assert cube.shape[0] == 1

    # print('cube:', cube)

    for _ in range(cycle_count):
        # add new z for the masking
        new_cube = np.zeros(tuple(map(sum, zip(cube.shape, itertools.cycle((4,))))))
        new_cube[tuple(slice(2, -2) for _ in cube.shape)] = cube
        cube = new_cube

        new_cube = np.zeros(tuple(map(sum, zip(cube.shape, itertools.cycle((-2,))))))

        for coord in itertools.product(*[range(1, s - 1) for s in cube.shape]):
            # TODO z, y, x
            # print('z:', z, 'y:', y, 'x:', x)
            me = cube[coord]
            neighbors = cube[tuple(slice(i - 1, i + 2) for i in coord)]
            assert neighbors.shape == tuple(3 for _ in cube.shape)
            neighbors = np.sum(neighbors, dtype='uint') - me
            if (me == True and neighbors in (2, 3)) or (me == False and neighbors == 3):
                # print('yes', z, y, x)
                new_cube[tuple(i - 1 for i in coord)] = True
            else:
                new_cube[tuple(i - 1 for i in coord)] = False

        cube = new_cube

        # print('cube:', cube)

    return np.sum(cube, dtype='uint')


def test_cycle():
    input_test = """.#.
..#
###"""
    cube = parse_cube(input_test)
    assert list(cube.reshape((9,))) == [False, True, False, False, False, True, True, True, True]
    assert cycle(cube, 6) == 112
    assert cycle(add_dim(cube), 6) == 848


if __name__ == '__main__':
    input_ = parse_cube(open('input.txt').read())
    print('part1:', cycle(input_, 6))
    print('paatr2:', cycle(add_dim(input_), 6))
