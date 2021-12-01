from operator import itemgetter

import numpy as np


input_test = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""



def parse(input_):
    tr = str.maketrans('.#', '01')
    state, rules = input_.rstrip('\n').split('\n\n')
    state = np.array([s == '#' for s in state.split('initial state: ')[1]], dtype='bool')

    rules = [(int(mask.translate(tr), base=2), result == '#')
             for mask, result in (ru.split(' => ') for ru in rules.split('\n'))]

    rules_index = np.zeros(32, dtype='bool')
    for i, r in rules:
        rules_index[i] = r

    return state, rules_index


def print_state(state, offset=0):
    print(' ' * offset + '0')
    print(''.join('#' if s else '.' for s in state))


def generate(input_, genth):
    state, rules = input_

    offset = 0
    offset_per_gen = 0
    g = 0
    for g in range(genth):
        # surround state with extra empty pots
        new_state = np.zeros(len(state) + 8, dtype='bool')
        new_state[4:-4] = state
        offset += 2
        state = new_state

        # result state
        new_state = np.zeros(len(state) - 4, dtype='bool')

        # process the next generation
        for i in range(2, len(state) - 2):
            mask = int(''.join('1' if s else '0' for s in state[i - 2:i + 3]), base=2)
            new_state[i - 2] = rules[mask]

        zero_state = np.trim_zeros(state)
        zero_new_state = np.trim_zeros(new_state)
        idx_offset = np.argmax(new_state) - np.argmax(state)
        state = new_state
        if zero_state.shape == zero_new_state.shape and (zero_state == zero_new_state).all():
            offset_per_gen = idx_offset
            break

    # print_state(state, offset)

    indexes = np.where(state == True)[0] - (offset + offset_per_gen * (genth - g - 1))

    return indexes


def test_generate():
    input_ = parse(input_test)

    results = """...#..#.#..##......###...###...........
...#...#....#.....#..#..#..#...........
...##..##...##....#..#..#..##..........
..#.#...#..#.#....#..#..#...#..........
...#.#..#...#.#...#..#..##..##.........
....#...##...#.#..#..#...#...#.........
....##.#.#....#...#..##..##..##........
...#..###.#...##..#...#...#...#........
...#....##.#.#.#..##..##..##..##.......
...##..#..#####....#...#...#...#.......
..#.#..#...#.##....##..##..##..##......
...#...##...#.#...#.#...#...#...#......
...##.#.#....#.#...#.#..##..##..##.....
..#..###.#....#.#...#....#...#...#.....
..#....##.#....#.#..##...##..##..##....
..##..#..#.#....#....#..#.#...#...#....
.#.#..#...#.#...##...#...#.#..##..##...
..#...##...#.#.#.#...##...#....#...#...
..##.#.#....#####.#.#.#...##...##..##..
.#..###.#..#.#.#######.#.#.#..#.#...#..
.#....##....#####...#######....#.#..##."""
    results = [[i - 3 for i, v in enumerate(r) if v == '#']
               for r in results.split('\n')]

    for g in range(20):
        assert list(generate(input_, g)) == results[g]

    assert 325 == np.sum(generate(parse(input_test), 20))


if __name__ == '__main__':
    input_ = parse(open('input.txt').read())
    print('part1:', np.sum(generate(input_, 20)))

    # for g in range(95):
    #     print('g:', g, np.sum(generate(input_, g)))
    print('part2:', np.sum(generate(input_, 50000000000)))
