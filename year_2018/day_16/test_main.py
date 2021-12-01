import operator
from collections import namedtuple, defaultdict


Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])


class Machine(object):
    operators = {'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori'}
    comparisons = {'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'}
    assignments = {'setr', 'seti'}
    instructions = operators | comparisons | assignments

    def __init__(self):
        self.registers = [0 for _ in range(4)]

    def set(self, a=None, b=None, c=None, d=None):
        if a is not None:
            self.registers[0] = a
        if b is not None:
            self.registers[1] = b
        if c is not None:
            self.registers[2] = c
        if d is not None:
            self.registers[3] = d

    def run_instruction(self, i):
        assert isinstance(i.opcode, str) and len(i.opcode) == 4
        assert isinstance(i.a, int)
        assert isinstance(i.b, int)
        assert isinstance(i.c, int)


        if i.opcode in self.operators:
            read_a, read_b = ('r', i.opcode[-1])
            op = {
                'add': operator.add,
                'mul': operator.mul,
                'ban': operator.and_,
                'bor': operator.or_,
            }[i.opcode[:-1]]
        elif i.opcode in self.comparisons:
            read_a, read_b = tuple(i.opcode[-2:])
            op = {
                'gt': operator.gt,
                'eq': operator.eq,
            }[i.opcode[:-2]]
        elif i.opcode in self.assignments:
            read_a, read_b = (i.opcode[-1], 'i')
            op = lambda a, b: a
        else:
            raise RuntimeError('Invalid opcode')

        a = i.a
        if read_a == 'r':
            if a not in (0, 1, 2, 3):
                raise RuntimeError('Invalid reading register A')
            a = self.registers[a]
        b = i.b
        if read_b == 'r':
            if b not in (0, 1, 2, 3):
                raise RuntimeError('Invalid reading register B')
            b = self.registers[b]

        if i.c not in (0, 1, 2, 3):
            raise RuntimeError('Invalid writing register C')

        self.registers[i.c] = op(a, b)


def find_possible_instructions(before, instruction, after):
    m = Machine()

    result = set()
    for i in m.instructions:
        m.set(*before)
        try:
            m.run_instruction(Instruction(i, *instruction[1:]))
        except RuntimeError:
            continue

        if m.registers == after:
            result.add(i)

    return result


def test_find_possible_instructions():
    assert find_possible_instructions(
        [3, 2, 1, 1],
        Instruction(9, 2, 1, 2),
        [3, 2, 2, 1],
    ) == {'mulr', 'addi', 'seti'}


def parse(input_):
    samples, program = input_.rstrip('\n').split('\n\n\n\n')

    samples = [(
        list(map(int, before.split('Before:')[1].strip()[1:-1].split(', '))),
        Instruction(*list(map(int, instruction.split(' ')))),
        list(map(int, after.split('After:')[1].strip()[1:-1].split(', '))),
    ) for before, instruction, after in (
        s.split('\n') for s in samples.split('\n\n')
    )]

    return samples, program


def test_parse():
    input_ = """Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]



6 1 3 1"""

    assert parse(input_) == (
        [([3, 2, 1, 1], Instruction(9, 2, 1, 2), [3, 2, 2, 1])],
        '6 1 3 1',
    )


def part1(samples, _):
    return sum(len(find_possible_instructions(*s)) >= 3 for s in samples)


def part2(samples, test_program):
    opcode_candidates = defaultdict(set)
    for b, i, a in samples:
        opcode_candidates[i.opcode] |= find_possible_instructions(b, i, a)

    # remove the defaultdict behavior
    opcode_candidates = dict(opcode_candidates)


    opcodes = dict()

    while opcode_candidates:
        for o, c in opcode_candidates.items():
            if len(c) != 1:
                continue

            opcodes[o] = c.pop()

        found_opcodes = set(opcodes.values())

        opcode_candidates = {o: c - found_opcodes
                             for o, c in opcode_candidates.items()}
        opcode_candidates = {o: c
                             for o, c in opcode_candidates.items()
                             if c}

    # parse input program
    instructions = [tuple(map(int, i.split(' ')))
                    for i in test_program.split('\n')]

    # translate the opcode into instructions names
    instructions = [Instruction(opcodes[i[0]], *i[1:]) for i in instructions]

    # execute the program
    m = Machine()
    for i in instructions:
        m.run_instruction(i)

    return m.registers[0]


if __name__ == '__main__':
    input_ = parse(open('input.txt').read())
    print('part1:', part1(*input_))
    print('part2:', part2(*input_))
