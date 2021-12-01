import operator
from functools import reduce
from collections import Counter

def count(str_):
    c = Counter(str_)
    has_two = has_three = False
    for k, v in c.items():
        if v == 2:
            has_two = True
        elif v == 3:
            has_three = True

    return (has_two, has_three)


def test_count():
    assert count('abcdef') == (0, 0)
    assert count('bababc') == (1, 1)
    assert count('abbcde') == (1, 0)
    assert count('abcccd') == (0, 1)
    assert count('aabcdd') == (1, 0)
    assert count('abcdee') == (1, 0)
    assert count('ababab') == (0, 1)


input_test = """abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab"""

def mul(input_):
    return reduce(
        operator.mul,
        reduce(
            (lambda a, b: (a[0] + b[0], a[1] + b[1])),
            map(count, input_.rstrip('\n').split('\n')),
            (0, 0),
        ),
        1,
    )

def test_mul():
    assert mul(input_test) == 12


def common_letters(input_):
    input_ = input_.rstrip('\n').split('\n')
    for i in input_:
        for j in input_:
            if i == j:
                continue

            if sum(a != b for a, b in zip(i, j)) == 1:
                # print('matches:', i, j, ''.join(set(i) & set(j)))

                return ''.join(a for a, b in zip(i, j) if a == b)


def test_common_letters():
    input_ = """abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz"""
    assert common_letters(input_) == 'fgij'



if __name__ == '__main__':
    input_ = open('input.txt').read()

    print('mul:', mul(input_))
    print('common:', common_letters(input_))
