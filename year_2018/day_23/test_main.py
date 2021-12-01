from operator import itemgetter, sub, add
from collections import namedtuple

import z3


class Nanobot(namedtuple('Nanobot', ['x', 'y', 'z', 'r'])):
    def in_distance(self, other):
        d = sum(abs(a - b) for a, b in zip(self[:3], other[:3]))
        return d <= self.r


def parse(input_):
    nanobots = []

    for n in input_.rstrip('\n').split('\n'):
        coord, radius = n.split('pos=<')[1].split('>, r=')
        coord = tuple(map(int, coord.split(',')))
        radius = int(radius)

        nanobots.append(Nanobot(*coord, radius))

    return nanobots


def part1(nanobots):
    max_ = max(nanobots, key=itemgetter(-1))

    return sum(max_.in_distance(n) for n in nanobots)


def part2(nanobots):
    o = z3.Optimize()
    x, y, z = z3.Int('x'), z3.Int('y'), z3.Int('z')

    def zabs(v):
        return z3.If(v > 0, v, -v)

    def in_distance(n):
        d = zabs(x - n.x) + zabs(y - n.y) + zabs(z - n.z)
        return z3.If(d <= n.r, 1, 0)

    all_in_distance = z3.Int('all_in_distance')
    distance_to_origin = z3.Int('distance_to_origin')

    o.add(all_in_distance == z3.Sum(*[in_distance(n) for n in nanobots]))
    o.add(distance_to_origin == zabs(x) + zabs(y) + zabs(z))

    a = o.maximize(all_in_distance)
    b = o.minimize(distance_to_origin)

    assert o.check()

    # print('x:', o.model()[x], 'y:', o.model()[y], 'z:', o.model()[z])

    return b.lower().as_long()


def test_part1():
    input_test = """pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1"""
    assert part1(parse(input_test)) == 7


def test_part2():
    input_test = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""
    assert part2(parse(input_test)) == 36


if __name__ == '__main__':
    input_ = parse(open('input.txt').read())

    print('part1:', part1(input_))
    print('part2:', part2(input_))
