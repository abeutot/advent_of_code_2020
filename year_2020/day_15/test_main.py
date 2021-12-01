from collections import defaultdict


def last_number(input_, last_index):
    last_time_spoken = {}
    for i, n in enumerate([int(i) for i in input_.split(',')]):
        last_time_spoken[n] = (i,)
        current_number = n

    def _add_time(t, n):
        l = last_time_spoken.get(n)
        if l is None:
            last_time_spoken[n] = (t,)
        else:
            last_time_spoken[n] = (t, l[0])

    for i in range(i + 1, last_index):
        last_time = last_time_spoken.get(current_number)
        assert last_time is not None
        if len(last_time) == 1:
            current_number = 0
            _add_time(i, 0)
            # print('i:', i, 'number:', current_number)
            continue

        penultimate, last = last_time
        current_number = penultimate - last
        _add_time(i, current_number)

        # print('i:', i, 'number:', current_number)

    return current_number



def test_last_number():
    input_test = '0,3,6'
    assert last_number(input_test, 2020) == 436


def test_last_number_part2():
    assert last_number('0,3,6', 30000000) == 175594
    assert last_number('1,3,2', 30000000) == 2578
    assert last_number('2,1,3', 30000000) == 3544142
    assert last_number('1,2,3', 30000000) == 261214
    assert last_number('2,3,1', 30000000) == 6895259
    assert last_number('3,2,1', 30000000) == 18
    assert last_number('3,1,2', 30000000) == 362


if __name__ == '__main__':
    input_ = '0,20,7,16,1,18,15'
    print('2020th:', last_number(input_, 2020))
    print('30000000th:', last_number(input_, 30000000))
