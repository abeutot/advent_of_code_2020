from collections import defaultdict

DIRECTIONS = {'N': -1+1j, 'n': 1j, 'e': 1, 'w': -1, 'S': -1j, 's': 1-1j}

def setup_tiling(input_):
    input_ = input_.replace(
        'nw',
        'N',
    ).replace(
        'ne',
        'n',
    ).replace(
        'sw',
        'S',
    ).replace(
        'se',
        's',
    )
    to_flip = input_.rstrip('\n').split('\n')

    # we use a two value coordinate system
    # see https://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/AV0405/MARTIN/Hex.pdf
    tiles = defaultdict(bool)  # False is white and True is black

    # N <=> nw
    # n <=> ne
    # S <=> sw
    # s <=> se

    for f in to_flip:
        pos = 0

        for d in f:
            # make sure the tiles and the ones adadjacent to it exists
            tiles[pos]
            for n in DIRECTIONS.values():
                tiles[pos + n]

            pos += DIRECTIONS[d]
        else:
            tiles[pos] = not tiles[pos]

    return tiles


def flip_it(tiles, count):
    for i in range(count):
        to_flip = []

        # add a neighbors layer arround black tiles before each iteration
        for pos, color in list(tiles.items()):
            if not color:
                continue
            for n in DIRECTIONS.values():
                tiles[pos + n]

        for pos, color in list(tiles.items()):
            neighbors = list(DIRECTIONS.values())
            # print('neighbors:', pos, color, sum(tiles.get(n, False) for n in neighbors))
            neighbors = sum(tiles[pos + n] for n in neighbors)

            # if black
            if color and (neighbors == 0 or neighbors > 2):
                to_flip.append(pos)
            elif not color and neighbors == 2:
                to_flip.append(pos)

        for pos in to_flip:
            tiles[pos] = not tiles[pos]

        print('day %d: %d' % (i + 1, sum(tiles.values())))

    return tiles


def test_everything():
    input_test = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

    tiles = setup_tiling(input_test)
    assert sum(tiles.values()) == 10

    tiles = flip_it(tiles, 100)
    assert sum(tiles.values()) == 2208


if __name__ == '__main__':
    input_ = open('input.txt').read()
    tiles = setup_tiling(input_)
    print('part1:', sum(tiles.values()))
    tiles = flip_it(tiles, 100)
    print('part2:', sum(tiles.values()))
