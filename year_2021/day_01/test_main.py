def count_increases(measurements):
    return sum(
        m2 < m1
        for m1, m2 in zip(measurements, [measurements[0]] + measurements)
    )


def test_count_increases():
    assert count_increases([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]) == 7


if __name__ == '__main__':
    with open('input.txt') as f:
        print('answer:', count_increases(list(map(int, f.read().strip().split('\n')))))
