import re
import operator
import itertools
from collections import defaultdict
from functools import partial, reduce

from lark import Lark


input_test = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


input_test2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""


def parse(input_):
    input_rules, messages = input_.rstrip('\n').split('\n\n')

    messages = messages.split('\n')

    rules = {}

    for r in input_rules.split('\n'):
        parent, children = r.split(': ')

        parent = int(parent)

        # terminal rule
        if children.startswith('"'):
            assert children.endswith('"')
            children = children.strip('"')
            assert len(children) == 1
            assert not children.isdigit()
        else:
            children = [tuple(map(int, c.split(' '))) for c in children.split(' | ')]

        rules[parent] = children

    return rules, messages


def test_parse():
    assert parse(input_test) == (
        {
            0: [(4, 1, 5)],
            1: [(2, 3), (3, 2)],
            2: [(4, 4), (5, 5)],
            3: [(4, 5), (5, 4)],
            4: 'a',
            5: 'b',
        },
        ['ababbb', 'bababa', 'abbbab', 'aaabbb', 'aaaabbb'],
    )


def build_regex(rules, start=0):
    builder = partial(build_regex, rules)

    regex_rules = rules[start]

    if isinstance(regex_rules, str):
        return regex_rules

    regex = '(' + '|'.join(''.join(map(builder, r)) for r in regex_rules) + ')'

    if start == 0:
        regex = '^' + regex + '$'

    return regex


def test_build_regex():
    assert build_regex(parse(input_test)[0]) == r'^(a((aa|bb)(ab|ba)|(ab|ba)(aa|bb))b)$'


def match(rules, messages):
    regex = re.compile(build_regex(rules))

    return sum(regex.match(m) is not None for m in messages)


def test_match():
    rules, messages = parse(input_test)
    assert match(rules, messages) == 2


def match2(rules, messages):
    gr = []
    for ru, p in rules.items():
        productions = []
        for pr in p:
            if isinstance(pr, str):
                productions.append('"%s"' % pr)
                continue
            productions.append(' '.join('r%s' % i for i in pr))
        gr.append('r%s : %s' % (ru, ' | '.join(productions)))

    gr = '\n'.join(gr)
    # print(gr)
    gr = Lark(gr, start='r0')

    def is_valid(str_):
        try:
            gr.parse(str_)
        except Exception:
            return False
        else:
            return True

    return sum(is_valid(m) for m in messages)


def test_match2():
    assert match2(*parse(input_test)) == 2

    rules, messages = parse(input_test2)
    assert match(rules, messages) == 3
    assert match2(rules, messages) == 3

    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]
    assert match2(rules, messages) == 12


if __name__ == '__main__':
    rules, messages = parse(open('input.txt').read())
    print('part1:', match(rules, messages))

    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]
    print('part2:', match2(rules, messages))
