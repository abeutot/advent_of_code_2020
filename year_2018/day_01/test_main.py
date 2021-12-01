import itertools


def compute_frequency(input_):
    return sum(map(int, input_.split(', ')))


def test_samples():
    assert compute_frequency('+1, -2, +3, +1') == 3
    assert compute_frequency('+1, +1, +1') == 3
    assert compute_frequency('+1, +1, -2') == 0
    assert compute_frequency('-1, -2, -3') == -6


def find_duplicate(input_):
    already_reached = {0}

    current_frequency = 0

    for i in itertools.cycle(map(int, input_.split(', '))):
        current_frequency += i

        if current_frequency in already_reached:
            return current_frequency

        already_reached.add(current_frequency)

    raise


if __name__ == '__main__':
    input_ = ', '.join(open('input.txt').read().rstrip('\n').split('\n'))
    print(compute_frequency(input_))

    print(find_duplicate(input_))
