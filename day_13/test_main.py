import itertools
from operator import mul
from functools import reduce

import numpy as np


def earliest_bus(input_):
    departure, busses = input_.rstrip('\n').split('\n')
    departure = int(departure)
    busses = [int(b) for b in busses.split(',') if b != 'x']

    for ts in itertools.count(departure):
        for b in busses:
            if ts % b == 0:
                return b, ts - departure

    # unreachable because of infinite loop


input_test = """939
7,13,x,x,59,x,31,19"""
def test_earliest_bus():
    assert earliest_bus(input_test) == (59, 5)


def euclide(a, b):
    # https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu#Pseudo-code
    r, u, v, r_, u_, v_ = a, 1, 0, b, 0, 1
    while r_ != 0:
        q = r // r_
        r, u, v, r_, u_, v_ = r_, u_, v_, r - q * r_, u - q * u_, v - q * v_

    print('r:', r, 'u:', u, 'v:', v)
    return r, u, v


def test_euclide():
    assert euclide(120, 23) == (1, -9, 47)
    assert euclide(23, 120) == (1, 47, -9)


def chinese_theorem(remainders, modulos):
    # print('remainders:', remainders)
    # print('modulos:', modulos)

    N = reduce(mul, modulos, 1)
    # print('N:', N)

    n_hat = [N // n for n in modulos]
    # print('n_hat:', n_hat)

    e = [euclide(n, n_)[2] * n_ for n, n_ in zip(modulos, n_hat)]
    # e = [next(i * n_ for i in itertools.count(1) if (i * n_) % m == 1) for n_, m in zip(n_hat, modulos)]
    # print('e:', e)

    x = sum(r * i for r, i in zip(remainders, e))

    return x % N


def test_chinese_theorem():
    assert chinese_theorem([2, 3, 2], [3, 5, 7]) == 23
    assert chinese_theorem([1, 2, 3], [3, 5, 7]) == 52
    assert chinese_theorem([5, 3, 10], [7, 11, 13]) == 894
    assert chinese_theorem([3, 4, 5], [17, 11, 6]) == 785


def earliest_consecutive_departures(input_):
    _, busses = input_.rstrip('\n').split('\n')
    busses = [int(b) if b != 'x' else 'x' for b in busses.split(',')]

    index_max = len(busses) - 1

    remainders = [i % b for i, b in zip(range(index_max, -1, -1), busses) if b != 'x']

    return chinese_theorem(remainders, [b for b in busses if b != 'x']) - index_max


def test_earliest_consecutive_departures():
    assert earliest_consecutive_departures(input_test) == 1068781


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('earliest:', reduce(mul, earliest_bus(input_)))
    print('earlist consecutive:', earliest_consecutive_departures(input_))
