import sys

import pytest


class World(object):
    def __init__(self, regex):
        assert regex[0] == '^' and regex[-1] == '$'

        self.regex = regex
        self.map_ = {}
        self.x, self.y = sys.maxsize, sys.maxsize
        self.X, self.Y = -sys.maxsize, -sys.maxsize

    def set_room(self, pos):
        self.x = min(int(pos.real), self.x)
        self.y = min(int(pos.imag), self.y)
        self.X = max(int(pos.real), self.X)
        self.Y = max(int(pos.imag), self.Y)
        self.map_[pos] = '.'
        self.map_[pos - 1 -1j] = '#'
        self.map_[pos - 1 +1j] = '#'
        self.map_[pos + 1 -1j] = '#'
        self.map_[pos + 1 +1j] = '#'
        if pos - 1 not in self.map_:
            self.map_[pos - 1] = '?'
        if pos + 1 not in self.map_:
            self.map_[pos + 1] = '?'
        if pos - 1j not in self.map_:
            self.map_[pos - 1j] = '?'
        if pos + 1j not in self.map_:
            self.map_[pos + 1j] = '?'

    def generate(self):
        directions = {'N': -1j, 'S': 1j, 'W': -1, 'E': 1}

        re_pos = 1
        st = []
        s, e = None, set()
        currents = {0}

        while True:
            r = self.regex[re_pos]

            nc = currents
            currents = set()
            for pos in nc:
                self.set_room(pos)

            if r in 'NSWE':
                for pos in nc:
                    currents.add(pos + directions[r] * 2)

                    if r in 'NS':
                        self.map_[pos + directions[r]] = '-'
                    else:
                        self.map_[pos + directions[r]] = '|'

            else:
                if r == '(':
                    st.append((s, e))
                    s = nc
                    e = set()
                    assert not currents
                    currents = s

                if r == '|':
                    e |= nc
                    assert not currents
                    currents = s

                if r == ')':
                    e |= nc
                    assert not currents
                    currents = e
                    s, e = st.pop()

            if r == '$':
                break

            re_pos += 1

        # remaining ??? are walls
        for j in range(self.y - 1, self.Y + 2):
            for i in range(self.x - 1, self.X + 2):
                c = complex(i, j)
                if c not in self.map_ or self.map_[c] == '?':
                    self.map_[c] = '#'

    def shortest_path(self):
        # (pos, length)
        paths = [(0, 0)]

        visited = {0}

        max_len = 0
        more_than_1000 = 0

        while paths:
            prev_paths = paths
            paths = []

            for p, l in prev_paths:
                visited.add(p)

                max_len = max(max_len, l)

                if l >= 1000:
                    more_than_1000 += 1

                for np in (-1, 1, -1j, 1j):
                    if self.map_[p + np] in '-|':
                        np = p + np * 2
                        if np not in visited:
                            paths.append((np, l + 1))

        return max_len, more_than_1000

    def __str__(self):
        result = ''
        for j in range(self.y - 1, self.Y + 2):
            for i in range(self.x - 1, self.X + 2):
                if i == j == 0:
                    result += 'X'
                else:
                    result += self.map_[complex(i, j)]
            result += '\n'

        return result


@pytest.mark.parametrize('regex,result,doors', [
    ('^WNE$', """#####
#.|.#
#-###
#.|X#
#####\n""", 3),
    ('^ENWWW(NEEE|SSE(EE|N))$', """#########
#.|.|.|.#
#-#######
#.|.|.|.#
#-#####-#
#.#.#X|.#
#-#-#####
#.|.|.|.#
#########\n""", 10),
    ('^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$', """###########
#.|.#.|.#.#
#-###-#-#-#
#.|.|.#.#.#
#-#####-#-#
#.#.#X|.#.#
#-#-#####-#
#.#.|.|.|.#
#-###-###-#
#.|.|.#.|.#
###########\n""", 18),
    ('^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$', """#############
#.|.|.|.|.|.#
#-#####-###-#
#.#.|.#.#.#.#
#-#-###-#-#-#
#.#.#.|.#.|.#
#-#-#-#####-#
#.#.#.#X|.#.#
#-#-#-###-#-#
#.|.#.|.#.#.#
###-#-###-#-#
#.|.#.|.|.#.#
#############\n""", 23),
    ('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$', """###############
#.|.|.|.#.|.|.#
#-###-###-#-#-#
#.|.#.|.|.#.#.#
#-#########-#-#
#.#.|.|.|.|.#.#
#-#-#########-#
#.#.#.|X#.|.#.#
###-#-###-#-#-#
#.|.#.#.|.#.|.#
#-###-#####-###
#.|.#.|.|.#.#.#
#-#-#####-#-#-#
#.#.|.|.|.#.|.#
###############\n""", 31),
])
def test_generate(regex, result, doors):
    w = World(regex)
    w.generate()

    assert str(w) == result
    assert w.shortest_path() == doors


if __name__ == '__main__':
    regex = open('input.txt').read().strip()
    w = World(regex)
    w.generate()
    print(w)
    part1, part2 = w.shortest_path()
    print('part1:', part1)
    print('part2:', part2)
