import operator
from enum import Enum
from functools import reduce
from collections import namedtuple


test_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


class Direction(Enum):
    FORWARD = 'forward'
    DOWN = 'down'
    UP = 'up'


Position = namedtuple('Position', ['horizontal', 'depth'])
Instruction = namedtuple('Instruction', ['direction', 'offset'])


def parse(input_):
    lines = input_.strip().split('\n')
    return [Instruction(Direction(d), int(o))
            for d, o in map(lambda l: l.split(), lines)]


def test_parse():
    assert parse(test_input) == [
        Instruction(Direction.FORWARD, 5),
        Instruction(Direction.DOWN, 5),
        Instruction(Direction.FORWARD, 8),
        Instruction(Direction.UP, 3),
        Instruction(Direction.DOWN, 8),
        Instruction(Direction.FORWARD, 2),
    ]


def compute_final_position(instructions):
    current = Position(0, 0)

    for d, o in instructions:
        if d == Direction.FORWARD:
            current = Position(current.horizontal + o, current.depth)
            continue

        if d == Direction.DOWN:
            current = Position(current.horizontal, current.depth + o)
            continue

        if d == Direction.UP:
            current = Position(current.horizontal, current.depth - o)
            continue

    return reduce(operator.mul, current)


def test_compute_final_position():
    assert compute_final_position(parse(test_input)) == 150


if __name__ == '__main__':
    instructions = parse(open('input.txt').read())
    print('part1:', compute_final_position(instructions))
