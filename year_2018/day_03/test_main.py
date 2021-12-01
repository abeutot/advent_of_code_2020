import operator
from functools import reduce
from collections import defaultdict


def parse_input(input_):
    input_ = input_.rstrip('\n').split('\n')

    claims = []
    for l in input_:
        id_, at, from_, area = l.split()
        assert id_.startswith('#')
        assert at == '@'
        assert from_.endswith(':')
        id_ = id_[1:]
        from_ = tuple(map(int, from_[:-1].split(',')))
        area = tuple(map(int, area.split('x')))

        claims.append((id_, from_, area))


    fabric = [['.' for _ in range(1000)] for _ in range(1000)]

    for id_, (from_top, from_left), (area_height, area_width) in claims:
        for i in range(area_height):
            for j in range(area_width):
                current = fabric[i + from_top][j + from_left]
                if current != '.':
                    fabric[i + from_top][j + from_left] = 'X'
                else:
                    fabric[i + from_top][j + from_left] = id_
    return claims, fabric


def overlap(input_):
    _, fabric = parse_input(input_)

    return sum(1 for i in fabric for j in i if j == 'X')


input_test = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""
def test_overlap():
    assert overlap(input_test) == 4


def non_overlap_claim(input_):
    claims, fabric = parse_input(input_)

    fabric_areas = defaultdict(int)

    for i in fabric:
        for j in i:
            if j == '.' or j == 'X':
                continue
            fabric_areas[j] += 1

    for id_, _, area in claims:
        area = reduce(operator.mul, area, 1)

        fabric_area = fabric_areas[id_]

        if fabric_area == area:
            return id_


def test_non_overlap():
    assert non_overlap_claim(input_test) == '3'



if __name__ == "__main__":
    input_ = open('input.txt').read()
    print('overlap:', overlap(input_))
    print('non overlap:', non_overlap_claim(input_))
