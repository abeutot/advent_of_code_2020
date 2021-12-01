import operator
from collections import namedtuple, defaultdict


Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])


class Machine(object):
    operators = {'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori'}
    comparisons = {'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'}
    assignments = {'setr', 'seti'}
    instructions = operators | comparisons | assignments

    def __init__(self):
        self.registers = [0 for _ in range(6)]

        self.ip_register = None
        self.program = None

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
            if a not in (0, 1, 2, 3, 4, 5):
                raise RuntimeError('Invalid reading register A')
            a = self.registers[a]
        b = i.b
        if read_b == 'r':
            if b not in (0, 1, 2, 3, 4, 5):
                raise RuntimeError('Invalid reading register B')
            b = self.registers[b]

        if i.c not in (0, 1, 2, 3, 4, 5):
            raise RuntimeError('Invalid writing register C')

        self.registers[i.c] = op(a, b)

    def load_program(self, program):
        assert self.program is None

        program = program.rstrip('\n').split('\n')

        assert program[0].startswith('#ip ')
        self.ip_register = int(program[0].split(' ')[1])

        self.program = [Instruction(
            i[0],
            *tuple(map(int, i[1:])),
        ) for i in (p.split(' ') for p in program[1:])]

    def execute_program(self):
        past_registers = set()
        while 0 <= self.registers[self.ip_register] < len(self.program):
            self.run_instruction(self.program[self.registers[self.ip_register]])

            self.registers[self.ip_register] += 1

            h = hash(tuple(self.registers))
            if h in past_registers:
                import pdb;pdb.set_trace()
                break

            past_registers.add(h)


if __name__ == '__main__':
    """
    m = Machine()
    m.load_program(open('input.txt').read())
    m.execute_program()
    print('part1:', m.registers[0])
    """
    m = Machine()
    m.load_program(open('input.txt').read())
    m.registers[0] = 1
    m.execute_program()
    print('part2:', m.registers[0])
