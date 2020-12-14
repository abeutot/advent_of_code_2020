import itertools


def sum_(input_):
    input_ = input_.rstrip('\n').split('\n')

    instructions = [i.split(' = ') for i in input_]

    current_mask = None

    memory = {}

    for i, v in instructions:
        if i == 'mask':
            current_mask = v
            continue

        assert current_mask is not None
        assert i.startswith('mem[')

        addr = int(''.join(b for b in i if b.isdigit()))

        v = '{:b}'.format(int(v))
        v = '0' * (len(current_mask) - len(v)) + v

        assert len(current_mask) == len(v)

        v = [vv if m == 'X' else m for vv, m in zip(v, current_mask)]

        memory[addr] = int(''.join(v), 2)

    return sum(memory.values())


def test_sum_():
    input_ = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""
    assert sum_(input_) == 165


def sum_v2(input_):
    input_ = input_.rstrip('\n').split('\n')

    instructions = [i.split(' = ') for i in input_]

    current_mask = None

    memory = {}

    for i, v in instructions:
        if i == 'mask':
            current_mask = v
            continue

        assert current_mask is not None
        assert i.startswith('mem[')

        addr = '{:b}'.format(int(''.join(b for b in i if b.isdigit())))

        v = int(v)

        addr = '0' * (len(current_mask) - len(addr)) + addr
        assert len(current_mask) == len(addr)

        addr = [aa if m == '0' else m for aa, m in zip(addr, current_mask)]

        indexes = [i for i, b in enumerate(addr) if b == 'X']

        if not indexes:
            memory[int(''.join(addr), 2)] = v
            continue

        for r in itertools.product('01', repeat=len(indexes)):
            for i, b in zip(indexes, r):
                addr[i] = b
            memory[int(''.join(addr), 2)] = v

    return sum(memory.values())


def test_sum_v2():
    input_ = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""
    assert sum_v2(input_) == 208


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('sum:', sum_(input_))
    print('sum2:', sum_v2(input_))
