import itertools
from operator import itemgetter


def area(points):
    min_x = min(map(itemgetter(0), points))
    max_x = max(map(itemgetter(0), points))
    min_y = min(map(itemgetter(1), points))
    max_y = max(map(itemgetter(1), points))

    width = max_x - min_x
    height = max_y - min_y
    return width, height, width * height


def draw(points):
    print('-------------------------')
    min_x = min(map(itemgetter(0), points))
    max_x = max(map(itemgetter(0), points))
    min_y = min(map(itemgetter(1), points))
    max_y = max(map(itemgetter(1), points))

    grid = [['.' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

    for x, y, _, _ in points:
        grid[y - min_y][x - min_x] = '#'

    for r in grid:
        print(''.join(r))


def align_stars(input_):
    input_ = input_.rstrip('\n').replace('position=<', '').replace('> velocity=<', ',').replace('>', '').replace(' ', '')
    points = [tuple(map(int, l.split(','))) for l in input_.split('\n')]

    w, h, a = area(points)
    for i in itertools.count(1):
        # draw(points)
        # print('area:', w, h, a)
        npoints = [(x + vx, y + vy, vx, vy) for x, y, vx, vy in points]
        nw, nh, na = area(npoints)

        if na > a:
            break

        w, h, a = nw, nh, na
        points = npoints

    return i - 1, points


def test_align_stars():
    input_test = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""
    assert align_stars(input_test)[0] == 3


if __name__ == '__main__':
    input_ = open('input.txt').read()
    s, p = align_stars(input_)
    print('seconds:', s)
    draw(p)
