import string
import operator
from functools import reduce


def sum_of_group(str_):
    return len(set(l for l in str_ if l in string.ascii_lowercase))


def excl_sum_of_group(str_):
    return len(reduce(operator.and_, map(set, str_.split('\n')), set(string.ascii_lowercase)))


def split_groups(str_):
    return str_.split('\n\n')


input_test = """abc

a
b
c

ab
ac

a
a
a
a

b"""

def test_group():
    assert tuple(map(sum_of_group, split_groups(input_test))) == (3, 3, 3, 1, 1)


def test_excl_group():
    assert tuple(map(excl_sum_of_group, split_groups(input_test))) == (3, 0, 1, 1, 1)


if __name__ == '__main__':
    groups = split_groups(open('input.txt').read().rstrip())
    print('sum:', sum(map(sum_of_group, groups)))
    print('excl sum:', sum(map(excl_sum_of_group, groups)))
