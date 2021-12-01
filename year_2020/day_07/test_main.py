from operator import itemgetter
from collections import defaultdict


input_test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""


def input_to_dict(input_):
    bags = [l.rstrip('.').split(' contain ') for l in input_.strip().split('\n')]
    remove_bags = lambda b: b.replace(' bags', '').replace(' bag', '')
    bags = {remove_bags(k): tuple(map(remove_bags, v.split(', '))) for k, v in bags}
    into_numeric = lambda b: (int(b.split()[0]), b.split(' ', 1)[1])
    bags = {k: None if v == ('no other',) else tuple(map(into_numeric, v)) for k, v in bags.items()}
    return bags

# print(input_to_dict(input_test))

def can_contain(which, bags):
    reverse_index = defaultdict(set)
    for k, v in bags.items():
        if v is None:
            continue

        for vv in v:
            reverse_index[vv[1]].add(k)

    # print(reverse_index)

    containers = set()

    keys = [which]

    while keys:
        test = keys.pop()
        new_containers = reverse_index[test] - containers
        containers |= new_containers
        keys.extend(new_containers)

    return containers




def test_shiny_gold():
    bags = input_to_dict(input_test)

    containers = can_contain('shiny gold', bags)
    assert containers == {'bright white', 'muted yellow', 'dark orange', 'light red'}


input_test_must_contain = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


def must_contain(which, bags):
    result = 0

    if bags[which] is None:
        return 0

    # print('must_contain:', which, bags[which])

    for b in bags[which]:
        result += b[0] + b[0] * must_contain(b[1], bags)

    return result

    while to_explore:
        test = to_explore.pop()

        todo = bags[test]
        if todo is None:
            continue

        result += sum(map(itemgetter(0), todo))
        to_explore.extend(map(itemgetter(1), todo))

    return result


def test_must_contain_shiny_gold():
    bags = input_to_dict(input_test)
    assert 32 == must_contain('shiny gold', bags)
    bags = input_to_dict(input_test_must_contain)
    assert 126 == must_contain('shiny gold', bags)


if __name__ == '__main__':
    input_ = input_to_dict(open('input.txt').read().rstrip('\n'))
    print('can contain:', len(can_contain('shiny gold', input_)))
    print('must contain:', must_contain('shiny gold', input_))
