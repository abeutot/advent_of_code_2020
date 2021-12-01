import itertools
from pprint import pprint

import numpy as np
from tqdm import tqdm


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

def compare_lists(l1, l2):
    l1 = l1[l1.index('#'):]
    l2 = l2[l2.index('#'):]

    l1 = l1[::-1]
    l2 = l2[::-1]

    l1 = l1[l1.index('#'):]
    l2 = l2[l2.index('#'):]

    return l1 == l2



def generation(input_, gen_count, margin=4):
    state, notes = input_.rstrip('\n').split('\n\n')

    state = list(state.split('initial state: ')[1])

    notes = {tuple(a): b
             for a, b in (n.split(' => ')
                          for n in notes.split('\n'))}

    state = ['.'] * margin + state + ['.'] * margin
    gen = 0
    for gen in range(gen_count):
        # print(''.join(state))
        # print('len:', len(state))
        new_state = []
        for i in range(2, len(state) - 2):
            pattern = tuple(state[i - 2:i + 3])
            new_state.append(notes.get(pattern, '.'))
            # new_state.append(notes[pattern])
        new_state = ['.'] * (margin + 2) + new_state + ['.'] * (margin + 2)

        if compare_lists(new_state, state):
            gen += 1
            break
        state = new_state

    # print(''.join(state))
    # print('len:', len(state))
    # print('start idx:', -(gen_count + 1) * margin)
    # print('state:', ''.join(state))
    s = list(pi for pi, (i, p) in zip(itertools.count(-(gen + 1) * margin), enumerate(state)) if p == '#')
    # print('s:', s)
    return sum(s)


def generation_v2(input_, gen_count, margin=4):
    state, notes = input_.rstrip('\n').split('\n\n')

    tr = str.maketrans('.#', '01')
    state = np.array(
        list(map(int, state.split('initial state: ')[1].translate(tr))),
        dtype='bool',
    )

    notes = [(int(a.translate(tr), base=2), int(b.translate(tr), base=2))
             for a, b in (n.split(' => ')
                          for n in notes.split('\n'))]
    new_notes = np.zeros(32, dtype='bool')
    for n, r in notes:
        new_notes[n] = r
    notes = new_notes

    offset = 0

    exponents = np.array(list(map(lambda i: 2 ** i, range(4, -1, -1))), dtype='uint')
    for _ in tqdm(range(gen_count)):
        # print('begin loop')
        first = np.argmax(state)
        if first < 4:
            # print('extend begin', first)
            # add leading zeros because we need at least 4 of them for the
            # masking to work
            new_state = np.zeros(len(state) + 4, dtype='bool')
            new_state[4:len(state) + 4] = state
            state = new_state
            first = 2
            offset += 4
        else:
            first -= 2

        last = len(state) - (np.argmax(state[::-1]) + 1)
        if len(state) - last < 4:
            # print('extend last', last)
            # add trailing zeros for the same reason
            new_state = np.zeros(len(state) + 4, dtype='bool')
            new_state[0:len(state)] = state
            state = new_state
        last += 2

        len_ = last - first
        # print('off:', offset, 'first:', first, 'last:', last, 'len:', len_, 'real_len:', len(state))
        # print('state:', ''.join('#' if s == 1 else '.' for s in state))

        new_state = np.zeros(2 * margin + len_, dtype='bool')
        # offset += margin - 2
        offset = offset - first + margin

        for i, ni in zip(range(first, last), itertools.count(margin)):
            key = np.sum(state[i - 2:i + 3] * exponents)
            new_state[ni] = notes[key]

        state = new_state
        # print('off:', offset)
        # print('state:', ''.join('#' if s == 1 else '.' for s in state))
        # print('end loop\n')


    # print('\npfiou')
    # print('state:', ''.join('#' if s == 1 else '.' for s in state))
    # print('offset:', offset)
    # print()
    # return list(np.where(state == True)[0] - offset)
    return np.sum(np.where(state == True)[0] - offset)


def test_generations():
    result = [
        '...#..#.#..##......###...###...........',
        '...#...#....#.....#..#..#..#...........',
        '...##..##...##....#..#..#..##..........',
        '..#.#...#..#.#....#..#..#...#..........',
        '...#.#..#...#.#...#..#..##..##.........',
        '....#...##...#.#..#..#...#...#.........',
        '....##.#.#....#...#..##..##..##........',
        '...#..###.#...##..#...#...#...#........',
        '...#....##.#.#.#..##..##..##..##.......',
        '...##..#..#####....#...#...#...#.......',
        '..#.#..#...#.##....##..##..##..##......',
        '...#...##...#.#...#.#...#...#...#......',
        '...##.#.#....#.#...#.#..##..##..##.....',
        '..#..###.#....#.#...#....#...#...#.....',
        '..#....##.#....#.#..##...##..##..##....',
        '..##..#..#.#....#....#..#.#...#...#....',
        '.#.#..#...#.#...##...#...#.#..##..##...',
        '..#...##...#.#.#.#...##...#....#...#...',
        '..##.#.#....#####.#.#.#...##...##..##..',
        '.#..###.#..#.#.#######.#.#.#..#.#...#..',
        '.#....##....#####...#######....#.#..##.',
    ]
    for i, r in enumerate(result):
        # assert [idx - 3 for idx, p in enumerate(r) if p == '#'] == generation_v2(input_test, i)
        # continue
        count = sum(idx - 3 for idx, p in enumerate(r) if p == '#')
        assert count == generation(input_test, i)
        # assert count == generation_v2(input_test, i)


def test_generation():
    assert 325 == generation(input_test, 20)
    # assert 325 == generation_v2(input_test, 20)


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('20th:', generation_v2(input_, 20))
    print('50000000000th:', generation_v2(input_, 1000))
