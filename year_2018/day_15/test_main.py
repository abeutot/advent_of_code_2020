import itertools

import pytest


def parse(input_):
    map_, gobelins, elves = set(), set(), set()
    for y, l in enumerate(input_.split('\n')):
        for x, s in enumerate(l):
            if s == '#':
                continue

            pos = (x, y)

            assert s in 'GE.'

            if s == 'G':
                gobelins.add(pos)
            elif s == 'E':
                elves.add(pos)

            map_.add(pos)


    return (
        x + 1,
        y + 1,
        map_,
        gobelins,
        elves,
    )


def test_parse():
    assert parse("""#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""") == (
        7, 7,
        # available points on the map
        {(1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
         (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
         (1, 3), (3, 3), (5, 3),
         (1, 4), (2, 4), (3, 4), (5, 4),
         (1, 5), (2, 5), (3, 5), (4, 5), (5, 5)},
        # gobelins
        {(2, 1), (5, 2), (5, 3), (3, 4)},
        # elves
        {(4, 2), (5, 4)},
    )


def find_shortest_path(x, y, targets, available):
    visiting_paths = [[(x, y)]]
    visited = set()
    target_paths = {t: [] for t in targets}

    while visiting_paths:
        to_explore_next = []

        for p in visiting_paths:
            for j, i in itertools.product(range(-1, 2), range(-1, 2)):
                if abs(j) == abs(i):
                    continue

                pos = (p[-1][0] + i, p[-1][1] + j)
                if pos not in available or pos in visited:
                    continue

                visited.add(pos)

                new_p = p + [pos]

                if pos in targets:
                    target_paths[pos].append(new_p)
                    continue

                to_explore_next.append(new_p)

        visiting_paths = to_explore_next

    result_paths = list(itertools.chain.from_iterable(target_paths.values()))

    result_paths.sort(key=lambda p: (len(p), *tuple(reversed(p[-1]))))

    # print('shortest paths:', result_paths)

    if result_paths:
        return result_paths[0][1]

    return None


def combat(X, Y, map_, gobelins, elves, elf_damage=3):
    # keep live points for each unit
    gobelins = {k: 200 for k in gobelins}
    elves = {k: 200 for k in elves}

    assert gobelins or elves

    for round_ in itertools.count(1):
        # print('round:', round_)
        """
        print(' ' + ''.join(map(str, range(X))))
        for y in range(Y):
            print(str(y), end='')
            characters = []
            for x in range(X):
                if (x, y) not in map_:
                    print('#', end='')
                    continue
                if (x, y) in gobelins:
                    characters.append('G(%d)' % gobelins[(x, y)])
                    print('G', end='')
                    continue
                if (x, y) in elves:
                    characters.append('E(%d)' % elves[(x, y)])
                    print('E', end='')
                    continue
                print('.', end='')
            if characters:
                print('   ' + ', '.join(characters), end='')
            print()
        """

        # list all protagonists positions that we need to evaluate
        positions = list(sorted(
            itertools.chain(gobelins, elves),
            key=lambda t: tuple(reversed(t)),
        ))

        for idx, (x, y) in enumerate(positions):
            # print('coucou:', x, y)
            if (x, y) in elves:
                attack_damage = elf_damage
                team = elves
                enemies = gobelins
            elif (x, y) in gobelins:
                attack_damage = 3
                team = gobelins
                enemies = elves
            else:
                # it must have been killed during this round
                continue

            neighbors = [(x + i, y + j)
                         for i, j in itertools.product(range(-1, 2),
                                                       range(-1, 2))
                         if abs(i) != abs(j) and (x + i, y + j) in enemies]
            # print('x,y:', x, y, 'neighbors:', neighbors)

            # if no one to attack nearby, try to move
            if not neighbors:
                # calculate the target points (arround the enemies)
                targets = [(xx + i, yy + j)
                           for xx, yy in enemies
                           for i, j in itertools.product(range(-1, 2),
                                                         range(-1, 2))
                           if abs(i) != abs(j)]
                # print('x,y:', x, y, 'targets:', targets)

                target = find_shortest_path(
                    x, y,
                    targets,
                    map_ - set(itertools.chain(elves, gobelins)),
                )

                # print('x,y:', x, y, 'target:', target)

                # no target
                if target is None:
                    continue

                team[target] = team.pop((x, y))

                x, y = target

                # check if the protagonist has neighbors now that he moved
                neighbors = [(x + i, y + j)
                             for i, j in itertools.product(range(-1, 2),
                                                           range(-1, 2))
                             if abs(i) != abs(j) and (x + i, y + j) in enemies]

                if not neighbors:
                    # print('x,y:', x, y, 'cannot attack')
                    continue

            # print('x,y:', x, y, 'neighbors:', neighbors)

            # perform the attack on the (weakest, reading order)
            neighbors.sort(key=lambda p: (enemies[p], *tuple(reversed(p))))

            to_attack = neighbors[0]
            # print('x,y:', x, y, 'attack:', to_attack)
            enemies[to_attack] -= attack_damage

            # check if we killed the guy
            if enemies[to_attack] <= 0:
                # print('killed the guy :)', round_)
                del enemies[to_attack]
                if enemies is elves and elf_damage > 3:
                    # detect dead as soon as possible
                    return None

                # end of combat
                if not enemies:
                    break

        # if one team is dead, this is the end
        if not (gobelins and elves):
            if idx < len(positions) - 1:
                # the round didn't finish
                round_ -= 1
            break

    # print('round:', round_)
    return round_ * sum(itertools.chain(gobelins.values(), elves.values()))


@pytest.mark.parametrize("input_,expected", [
    (
        """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""",
        27730,
    ),
    (
        """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""",
        36334,
    ),
    (
        """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""",
        39514,
    ),
    (
        """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""",
        27755,
    ),
    (
        """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""",
        28944,
    ),
    (
        """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""",
        18740,
    ),
])
def test_combat(input_, expected):
    assert combat(*parse(input_)) == expected


def min_attack(X, Y, map_, gobelins, elves):
    for a in itertools.count(4):
        score = combat(X, Y, map_, gobelins, elves, a)
        if score is not None:
            return a, score


@pytest.mark.parametrize("input_,expected", [
    (
        """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""",
        (15, 4988),
    ),
    (
        """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""",
        (4, 31284),
    ),
    (
        """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""",
        (15, 3478),
    ),
    (
        """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""",
        (12, 6474),
    ),
    (
        """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""",
        (34, 1140),
    ),
])
def test_min_attack(input_, expected):
    assert min_attack(*parse(input_)) == expected


if __name__ == '__main__':
    input_ = parse(open('input.txt').read().rstrip('\n'))
    print('part1:', combat(*input_))
    print('part2:', min_attack(*input_))
