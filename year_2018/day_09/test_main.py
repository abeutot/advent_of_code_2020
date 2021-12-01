import itertools


def get_final_score(players_count, highest_marble):
    circle = [0]
    players_scores = [0 for _ in range(players_count)]

    current_marble = 0

    for m, p in zip(range(1, highest_marble + 1), itertools.cycle(range(players_count))):
        # print('circle:', circle, 'marble:', m, 'player:', p)
        if m % 23 == 0:
            players_scores[p] += m
            to_remove_index = (circle.index(current_marble) - 7) % len(circle)
            to_remove = circle[to_remove_index]
            players_scores[p] += to_remove
            circle = circle[:to_remove_index] + circle[to_remove_index + 1:]
            current_marble = circle[to_remove_index]
            continue

        current_index = circle.index(current_marble)
        split = (current_index + 1) % (len(circle)) + 1
        first = circle[:split]
        last = circle[split:]
        # print('current_idx:', current_index, 'first:', first, 'last:', last)
        circle = first + [m] + last

        current_marble = m

    return max(players_scores)


class CircularList(object):
    def __init__(self, value=0):
        self.next_ = self
        self.prev = self
        self.value = value

    def move(self, offset):
        if offset == 0:
            return self

        ret = self

        if offset < 0:
            for _ in range(offset, 0):
                ret = ret.prev
        elif offset > 0:
            for _ in range(0, offset):
                ret = ret.next_
        else:
            raise

        return ret

    def insert(self, value):
        new = self.__class__(value)

        if self.next_ is self:
            self.next_ = new
            new.next_ = self
            self.prev = new
            new.prev = self
        else:
            new.next_ = self.next_
            new.prev = self
            new.next_.prev = new
            self.next_ = new

        return new

    def remove(self):
        next_ = self.next_
        assert next_.value != self.value
        next_.prev = self.prev
        self.prev.next_ = next_
        return next_, self.value

    def __str__(self):
        start = self
        while start.value != 0:
            start = start.prev

        i = start
        output = []
        while True:
            if i is self:
                format_ = '(%d)'
            else:
                format_ = '%d'

            output.append(format_ % i.value)

            i = i.next_

            if i is start:
                break

        return ' '.join(output)


def get_final_score(players_count, highest_marble):
    circle = CircularList()
    players_scores = [0 for _ in range(players_count)]

    for m, p in zip(range(1, highest_marble + 1), itertools.cycle(range(players_count))):
        # print('circle:', circle, 'marble:', m, 'player:', p)
        if m % 23 == 0:
            players_scores[p] += m
            circle = circle.move(-7)
            circle, m = circle.remove()
            players_scores[p] += m
            continue

        circle = circle.move(1)
        circle = circle.insert(m)

    return max(players_scores)


def test_final_score():
    assert get_final_score(9, 25) == 32
    assert get_final_score(10, 1618) == 8317
    assert get_final_score(13, 7999) == 146373
    assert get_final_score(17, 1104) == 2764
    assert get_final_score(21, 6111) == 54718
    assert get_final_score(30, 5807) == 37305


if __name__ == '__main__':
    print('score:', get_final_score(476, 71657))
    print('score:', get_final_score(476, 71657 * 100))
