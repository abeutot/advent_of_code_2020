def parse(input_):
    return [(i, int(o))
            for i, o in (l.split() for l in input_.split('\n'))]


def run_until_infinite(instructions):
    instructions = [(i, o, 0) for i, o in instructions]
    accumulator = 0
    program_counter = 0

    while True:
        current_program_counter = program_counter
        try:
            i, o, c = instructions[program_counter]
        except IndexError:
            return accumulator, False

        print('pc:', program_counter, 'acc:', accumulator, 'instr:', i, 'offset:', o, 'count:', c)

        if c == 1:
            return accumulator, True

        if i == 'nop':
            program_counter += 1
        elif i == 'acc':
            program_counter += 1
            accumulator += o
        elif i == 'jmp':
            program_counter += o
        else:
            raise RuntimeError('unknown instruction')

        instructions[current_program_counter] = (i, o, c + 1)


input_test = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


def test_program():
    assert (5, True) == run_until_infinite(parse(input_test))


def run_altered(instructions):
    # brute force the program
    for idx, (instr, offset) in enumerate(instructions):
        if instr == 'acc':
            # print('line %d unchanged' % (idx,))
            continue

        print('alter line:', idx)

        instr = {'nop': 'jmp', 'jmp': 'nop'}[instr]

        acc, halted = run_until_infinite(instructions[:idx] + [(instr, offset)] + instructions[idx + 1:])

        if halted:
            continue

        return acc

    raise RuntimeError()


def test_unloop():
    assert 8 == run_altered(parse(input_test))



if __name__ == '__main__':
    input_program = parse(open('input.txt').read().rstrip('\n'))

    print('acc:', run_until_infinite(input_program)[0])

    print('acc:', run_altered(input_program))
