def count_increases(measurements):
    return sum(
        m2 < m1
        for m1, m2 in zip(measurements, [measurements[0]] + measurements)
    )


def count_increases_window(measurements):
    windows = [sum(i) for i in zip(measurements, measurements[1:], measurements[2:])]
    return count_increases(windows)


test_data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

def test_count_increases():
    assert count_increases(test_data) == 7


def test_count_increases_window():
    assert count_increases_window(test_data) == 5


if __name__ == '__main__':
    with open('input.txt') as f:
        input_ = list(map(int, f.read().strip().split('\n')))
        print('part1:', count_increases(input_))
        print('part2:', count_increases_window(input_))
