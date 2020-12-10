from operator import mul
from functools import reduce
from collections import defaultdict


def differences(input_):
    adapters = set(map(int, input_.rstrip('\n').split('\n')))
    adapters.add(max(adapters) + 3)

    diff_1 = 0
    diff_3 = 0

    jolt = 0
    while True:
        next_adapter = adapters & {jolt + 1, jolt + 2, jolt + 3}
        if not next_adapter:
            break
        next_adapter = min(next_adapter)
        if next_adapter - jolt == 1:
            diff_1 += 1
        elif next_adapter - jolt == 3:
            diff_3 += 1
        else:
            raise RuntimeError

        # print('next:', next_adapter, 'diff1:', diff_1, 'diff3:', diff_3)

        jolt = next_adapter

    return diff_1, diff_3


input_01 = """16
10
15
5
1
11
7
19
6
12
4"""
def test_differences_01():
    assert differences(input_01) == (7, 5)


input_02 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""
def test_differences_02():
    assert differences(input_02) == (22, 10)


def arrangements(input_):
    adapters = sorted(map(int, input_.rstrip('\n').split('\n')))

    combinations = defaultdict(int)
    combinations[0] = 1

    for a in adapters:
        sum_ = sum(combinations[i] for i in range(a - 3, a))
        combinations[a] = sum_

    return sum_


def test_arrangements_01():
    assert arrangements(input_01) == 8


def test_arrangements_02():
    assert arrangements(input_02) == 19208


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('part1:', reduce(mul, differences(input_), 1))
    print('part2:', arrangements(input_))
