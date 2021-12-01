import itertools


def step(recipes, elf1, elf2):
    # reworked to remove the recopy as it was too much intensive
    recipes.extend(map(int, str(recipes[elf1] + recipes[elf2])))
    return (
        recipes,
        (elf1 + 1 + recipes[elf1]) % len(recipes),
        (elf2 + 1 + recipes[elf2]) % len(recipes),
    )


def test_step():
    recipes = [3, 7]
    elf1, elf2 = 0, 1

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 0
    assert elf2 == 1
    assert recipes == [3, 7, 1, 0]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 4
    assert elf2 == 3
    assert recipes == [3, 7, 1, 0, 1, 0]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 6
    assert elf2 == 4
    assert recipes == [3, 7, 1, 0, 1, 0, 1]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 0
    assert elf2 == 6
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 4
    assert elf2 == 8
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 6
    assert elf2 == 3
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 8
    assert elf2 == 4
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 1
    assert elf2 == 6
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 9
    assert elf2 == 8
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 1
    assert elf2 == 13
    assert [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 9
    assert elf2 == 7
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 15
    assert elf2 == 10
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 4
    assert elf2 == 12
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 6
    assert elf2 == 2
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9]

    recipes, elf1, elf2 = step(recipes, elf1, elf2)
    assert elf1 == 8
    assert elf2 == 4
    assert recipes == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7, 7, 9, 2]


def next_10(nth):
    recipes = [3, 7]
    e1, e2 = 0, 1

    while len(recipes) < nth + 10:
        # print
        """
        for i, r in enumerate(recipes):
            format_ = ' %d '
            if i == e1:
                format_ = '(%d)'
            elif i == e2:
                format_ = '[%d]'
            print(format_ % r, end='')
        print()
        """
        # end print

        recipes, e1, e2 = step(recipes, e1, e2)

    return ''.join(map(str, recipes[nth:nth + 10]))


def test_next_10():
    assert next_10(9) == '5158916779'
    assert next_10(5) == '0124515891'
    assert next_10(18) == '9251071085'
    assert next_10(2018) == '5941429882'


def prev_10(pattern):
    pattern = list(map(int, pattern))

    recipes = [3, 7]
    e1, e2 = 0, 1

    for idx in itertools.count(0):
        if idx % 1000000 == 0:
            print('idx:', idx)

        while len(recipes) - idx < len(pattern):
            recipes, e1, e2 = step(recipes, e1, e2)

        if recipes[idx:idx + len(pattern)] == pattern:
            return idx


def test_prev_10():
    assert prev_10('51589') == 9
    assert prev_10('01245') == 5
    assert prev_10('92510') == 18
    assert prev_10('59414') == 2018


if __name__ == '__main__':
    print('part1:', next_10(77201))
    print('part2:', prev_10('077201'))
