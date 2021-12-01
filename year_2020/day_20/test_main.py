import itertools
from functools import reduce
from collections import defaultdict
from operator import mul, itemgetter

import numpy as np


input_test = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""


def parse(input_):
    images = input_.rstrip('\n').split('\n\n')

    images = [i.split('\n') for i in images]

    images = [(''.join(c for c in i[0] if c.isdigit()), i[1:]) for i in images]

    images = [(int(i), np.array([[d == '#' for d in dd] for dd in data], dtype='bool'))
              for i, data in images]

    # print('images:', images)

    return images


def get_images_borders(images):
    borders = defaultdict(list)

    for id_, data in images:
        borders[tuple(data[0,:])].append(id_)
        borders[tuple(data[-1,:])].append(id_)
        borders[tuple(data[:,0])].append(id_)
        borders[tuple(data[:,-1])].append(id_)
        borders[tuple(data[0,::-1])].append(id_)
        borders[tuple(data[-1,::-1])].append(id_)
        borders[tuple(data[::-1,0])].append(id_)
        borders[tuple(data[::-1,-1])].append(id_)

    border_images = defaultdict(int)

    for i in borders.values():
        if len(i) == 2:
            continue

        assert len(i) == 1

        border_images[i[0]] += 1

    return (
        [i for i, c in border_images.items() if c == 4],  # corners
        [i for i, c in border_images.items() if c == 2],  # borders
        borders,
    )


def corners(images):
    corners, _, _ = get_images_borders(images)

    # print('corners:', corners)
    return reduce(
        mul,
        corners,
        1,
    )


def test_corners():
    assert corners(parse(input_test)) == 20899048083289


def left(tile):
    return tile[:, 0]


def top(tile):
    return tile[0, :]


def right(tile):
    return tile[:, -1]


def bottom(tile):
    return tile[-1, :]


def assemble_image(images):
    corners, borders, joints = get_images_borders(images)

    images = dict(images)

    left_top_id, *corners = corners

    X, Y = 0, 0
    image_map = dict()
    # find out the borders of the tile
    tile = images[left_top_id]
    while True:
        l, t, r, b = (
            len(joints[tuple(left(tile))]) == 1,
            len(joints[tuple(top(tile))]) == 1,
            len(joints[tuple(right(tile))]) == 1,
            len(joints[tuple(bottom(tile))]) == 1,
        )

        if l and t:
            assert not b and not r
            image_map[(0, 0)] = (left_top_id, tile.T)
            break

        tile = np.rot90(tile)

    for i in itertools.count(1):
        previous_id, previous_tile = image_map[(i - 1, 0)]

        r = right(previous_tile)

        matching_id = set(joints[tuple(r)]) - {previous_id}
        assert len(matching_id) == 1
        matching_id = matching_id.pop()
        matching_tile = images[matching_id]

        while True:
            l = left(matching_tile)

            if np.all(r == l):
                image_map[(i, 0)] = (matching_id, matching_tile)
                break

            if np.all(r == l[::-1]):
                image_map[(i, 0)] = (matching_id, matching_tile[::-1, :])
                break

            matching_tile = np.rot90(matching_tile)

        if matching_id in corners:
            corners.remove(matching_id)
            X = i + 1
            break

    for j in itertools.count(1):
        for i in range(X):
            upper_id, upper_tile = image_map[(i, j - 1)]

            b = bottom(upper_tile)

            matching_id = set(joints[tuple(b)]) - {upper_id}
            assert len(matching_id) == 1
            matching_id = matching_id.pop()
            matching_tile = images[matching_id]

            while True:
                t = top(matching_tile)

                if np.all(b == t):
                    image_map[(i, j)] = (matching_id, matching_tile)
                    break

                if np.all(b == t[::-1]):
                    matching_tile = matching_tile[:, ::-1]
                    image_map[(i, j)] = (matching_id, matching_tile)
                    break

                matching_tile = np.rot90(matching_tile)
        else:
            # last tile has one border
            assert len(joints[tuple(right(matching_tile))]) == 1

        if matching_id in corners and i != 0:
            Y = j + 1
            break

    """
    # visualize ids
    for y in range(Y):
        for x in range(X):
            print(image_map[(x, y)][0], end='\t')
        print()

    # visualize tiles
    for y in range(Y):
        for j in range(image_map[(0, y)][1].shape[1]):
            print(' '.join(''.join('#' if i else '.' for i in image_map[(x, y)][1][j,:]) for x in range(X)))
        print()
    """

    tile_size = {i[1].shape for i in image_map.values()}
    assert len(tile_size) == 1
    tx, ty = tile_size.pop()
    tx, ty = tx - 2, ty - 2

    image = np.zeros((tx * X, ty * Y), dtype='bool')

    for x, y in itertools.product(*[range(X), range(Y)]):
        image[y * ty:(y + 1) * ty, x * tx:(x + 1) * tx] = image_map[(x, y)][1][1:-1,1:-1]

    """
    # visualize assembled image
    for y in range(image.shape[1]):
        for x in range(image.shape[0]):
            print('#' if image[(x, y)] else '.', end='')
        print()
    """

    return image


sea_monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
sea_monster = tuple((x, y)
                    for y, l in enumerate(sea_monster.split('\n'))
                    for x, v in enumerate(l)
                    if v == '#')
def water_roughness(images):
    image = assemble_image(images)
    X, Y = image.shape

    smx = max(map(itemgetter(0), sea_monster)) + 1
    smy = max(map(itemgetter(1), sea_monster)) + 1

    count_ = 0
    for s in map(lambda s: (slice(None, None, s[0]), slice(None, None, s[1])), itertools.product(*[(None, -1)], repeat=2)):
        simage = image[s]
        for _ in range(4):
            for x, y in itertools.product(*[range(X - smx + 1), range(Y - smy + 1)]):
                if all(simage[x + i, y + j] for i, j in sea_monster):
                    count_ += 1

            if count_ != 0:
                # that the total of sea monsters in this image
                print('total of %d sea monsters' % count_)
                return np.sum(image) - len(sea_monster) * count_

            simage = np.rot90(simage)

    raise RuntimeError('pattern not found')


def test_water_roughness():
    assert water_roughness(parse(input_test)) == 273


if __name__ == '__main__':
    input_ = parse(open('input.txt').read())
    print('part1:', corners(input_))
    print('part2:', water_roughness(input_))
