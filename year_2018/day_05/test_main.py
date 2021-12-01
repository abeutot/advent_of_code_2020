import string
import itertools
from operator import itemgetter
# import sys

# sys.setrecursionlimit(100000)


def polymerise(input_):
    # print('in:', input_)
    if len(input_) < 2:
        return input_

    first, second, *remain = input_

    if first.lower() == second.lower() and first != second:
        return polymerise(''.join(remain))

    remain = polymerise(''.join([second] + remain))

    if remain[0].lower() == first.lower() and first != remain[0]:
        return remain[1:]

    return first + remain


def polymerise(input_):
    while True:
        # print('i:', input_)
        keep = []
        i = 0
        while i < len(input_):
            if i == len(input_) - 1:
                keep.append(input_[i])
                i += 1
                continue

            a, b = input_[i], input_[i+1]

            if a != b and a.lower() == b.lower():
                i += 2
                continue

            keep.append(a)
            i += 1

        if keep == input_:
            break

        input_ = keep

    return ''.join(keep)


def test_polymerise():
    assert polymerise('aA') == ''
    assert polymerise('abBA') == ''
    assert polymerise('abAB') == 'abAB'
    assert polymerise('aabAAB') == 'aabAAB'
    assert polymerise('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'


def minimize_polymer(input_):
    lengths = [len(polymerise(input_.replace(l, '').replace(l.upper(), '')))
               for l in string.ascii_lowercase]

    return min(lengths)


def test_minimize():
    assert minimize_polymer('dabAcCaCBAcCcaDA') == 4


if __name__ == '__main__':
    input_ = open('input.txt').read().rstrip('\n')
    print(len(polymerise(input_)))
    print(minimize_polymer(input_))
