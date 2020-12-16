import itertools
from functools import reduce
from operator import itemgetter, mul


input_test = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


def parse_tickets(input_):
    fields, mine, nearby = input_.rstrip('\n').split('\n\n')

    fields = tuple((n,) + tuple(tuple(map(int, i.split('-'))) for i in r.split(' or ')) for n, r in (f.split(': ') for f in fields.split('\n')))

    mine = tuple(map(int, mine.split('your ticket:\n')[1].split(',')))

    nearby = tuple(tuple(map(int, r.split(','))) for r in nearby.split('nearby tickets:\n')[1].split('\n'))

    return fields, mine, nearby


def test_parse_tickets():
    assert parse_tickets(input_test) == (
        (
            ('class', (1, 3), (5, 7)),
            ('row', (6, 11), (33, 44)),
            ('seat', (13, 40), (45, 50)),
        ),
        (7, 1, 14),
        (
            (7, 3, 47),
            (40, 4, 50),
            (55, 2, 20),
            (38, 6, 12),
        ),
    )


def validate_tickets(fields, tickets):
    error_rate = 0

    rules = list(itertools.chain.from_iterable(map(lambda t: t[1:], fields)))
    fields = list(itertools.chain.from_iterable(tickets))

    rules.sort(key=itemgetter(0))
    fields.sort()

    merged_rules = []
    low, up = rules[0]
    for l, u in rules[1:]:
        if l <= up:
            up = u
            continue
        merged_rules.append((low, up))
        low, up = l, u
    merged_rules.append((low, up))
    rules = merged_rules

    # print('fields:', fields)
    # print('rules:', rules)
    rules = iter(rules)
    r_low, r_up = next(rules)
    for f in fields:
        while f > r_up:
            try:
                r_low, r_up = next(rules)
            except StopIteration:
                break

        if f < r_low or f > r_up:
            error_rate += f
            continue

    return error_rate


def filter_invalid_tickets(fields, tickets):
    return tuple(t
                 for t in tickets
                 if 0 == sum(1
                             for f in t
                             if sum(1
                                    for _, *r in fields
                                    for l, u in r
                                    if l <= f <= u) == 0))


def find_positions(fields, tickets):
    tickets = filter_invalid_tickets(fields, tickets)

    fields = list(fields)

    # find the possible positions for each column
    positions = []
    for i in range(len(tickets[0])):
        p = set()
        for n, *r in fields:
            valid_rows = sum(1 for f in map(itemgetter(i), tickets)
                               if 0 < sum(1 for l, u in r if l <= f <= u))
            # valid_rules = sum(1 for f in map(itemgetter(i), tickets)
            #                   if sum(1 for l, u in r if l <= f <= u))
            if valid_rows == len(tickets):  # and valid_rules == len(r):
                p.add(n)
        positions.append(p)

    # filter out the duplicate positions
    found = set()
    while len(found) != len(positions):
        new_positions = []
        for p in positions:
            if isinstance(p, str):
                new_positions.append(p)
                continue
            remain = p - found
            if len(remain) == 1:
                remain = remain.pop()
                found.add(remain)
                new_positions.append(remain)
                continue
            new_positions.append(remain)

        assert len(positions) == len(new_positions)
        positions = new_positions

    return tuple(positions)


def test_validate_tickets():
    r, _, t = parse_tickets(input_test)
    assert validate_tickets(r, t) == 71


def test_filter_invalid_tickets():
    r, _, n = parse_tickets(input_test)
    assert filter_invalid_tickets(r, n) == (
            (7, 3, 47),
    )


def test_find_positions():
    input_ = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    r, m, n = parse_tickets(input_)
    assert find_positions(r, (m,) + n) == ('row', 'class', 'seat')


if __name__ == '__main__':
    input_ = open('input.txt').read()
    fields, mine, nearby = parse_tickets(input_)
    print('#invalid tickets:', validate_tickets(fields, nearby))
    positions = find_positions(fields, (mine,) + nearby)
    result = reduce(mul, (v for f, v in zip(positions, mine) if f.startswith('departure')), 1)
    print('part2:', result)
