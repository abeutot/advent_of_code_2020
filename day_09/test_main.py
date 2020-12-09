input_test = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""


def non_valid(input_, preamble_length):
    input_ = list(map(int, input_.rstrip('\n').split('\n')))

    assert preamble_length < len(input_)

    for i, n in enumerate(input_):
        if i < preamble_length:
            continue

        preamble = input_[i - preamble_length:i]
        # print('preamble:', preamble)
        sums = {i + j for i in preamble for j in preamble if i != j}
        # print('sums:', sums)

        if n not in sums:
            return n

    raise


def test_non_valid():
    assert non_valid(input_test, 5) == 127


def find_sum(input_, which):
    input_ = list(map(int, input_.rstrip('\n').split('\n')))

    index = input_.index(which)

    input_ = input_[:index] + input_[index + 1:]

    for i, n in enumerate(input_):
        acc = n
        end = i + 1
        while acc < which and end < len(input_):
            acc += input_[end]
            end += 1

        if acc == which:
            return input_[i:end]

    raise RuntimeError('combination not found')


def test_find_sum():
    assert find_sum(input_test, non_valid(input_test, 5)) == [15, 25, 47, 40]


if __name__ == '__main__':
    input_ = open('input.txt').read()
    non_valid = non_valid(input_, 25)
    print('non valid:', non_valid)
    sum_ = find_sum(input_, non_valid)
    print('sum:', min(sum_), max(sum_), min(sum_) + max(sum_))
