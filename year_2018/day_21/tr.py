from collections import namedtuple


Instruction = namedtuple('Instruction', ['opcode', 'a', 'b', 'c'])


def translate(input_):
    input_ = input_.rstrip('\n')
    instructions = input_.split('\n')

    assert instructions[0].startswith('#ip ')
    ip_register = int(instructions[0].split(' ')[1])

    instructions = [Instruction(
        i[0],
        *tuple(map(int, i[1:])),
    ) for i in (p.split(' ') for p in instructions[1:])]

    for ip, i in enumerate(instructions):
        print('@%d\t' % ip, end='')
        if i.opcode == 'addi':
            print('R%d = R%d + %d' % (i.c, i.a, i.b))
        elif i.opcode == 'addr':
            print('R%d = R%d + R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'muli':
            print('R%d = R%d * %d' % (i.c, i.a, i.b))
        elif i.opcode == 'mulr':
            print('R%d = R%d * R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'bani':
            print('R%d = R%d & %d' % (i.c, i.a, i.b))
        elif i.opcode == 'borr':
            print('R%d = R%d | R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'bori':
            print('R%d = R%d | %d' % (i.c, i.a, i.b))
        elif i.opcode == 'banr':
            print('R%d = R%d & R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'seti':
            print('R%d = %d' % (i.c, i.a))
        elif i.opcode == 'setr':
            print('R%d = R%d' % (i.c, i.a))
        elif i.opcode == 'gtir':
            print('R%d = %d > R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'gtri':
            print('R%d = R%d > %d' % (i.c, i.a, i.b))
        elif i.opcode == 'gtrr':
            print('R%d = R%d > R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'eqir':
            print('R%d = %d == R%d' % (i.c, i.a, i.b))
        elif i.opcode == 'eqri':
            print('R%d = R%d == %d' % (i.c, i.a, i.b))
        elif i.opcode == 'eqrr':
            print('R%d = R%d == R%d' % (i.c, i.a, i.b))
        else:
            raise RuntimeError('bad instr')


if __name__ == '__main__':
    translate(open('input.txt').read())
