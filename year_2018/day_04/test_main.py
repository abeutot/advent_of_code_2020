from functools import reduce
from datetime import datetime
from operator import itemgetter, mul
from collections import defaultdict


input_test = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up"""


def parse_sleep_records(input_):
    input_ = input_.rstrip('\n').split('\n')
    records = []
    for i in input_:
        ts, event = i.split('] ')

        assert ts.startswith('[')
        ts = datetime.fromisoformat(ts[1:])

        if event.startswith('Guard ') and event.endswith(' begins shift'):
            event = '#' + event.split('#')[1].split()[0]

        records.append((ts, event))

    return sorted(records, key=itemgetter(0))


def create_usable_data(sleep_records):
    current_guard = None
    start_asleep = None

    total_sleep = defaultdict(int)
    most_asleep = defaultdict(lambda: defaultdict(int))

    for ts, e in sleep_records:
        # print('ts:', ts, 'e:', e)
        if e.startswith('#'):
            current_guard = int(e[1:])
            continue

        if current_guard is None:
            continue

        if e == 'falls asleep':
            start_asleep = ts
            continue

        assert start_asleep is not None
        if e == 'wakes up':
            total_sleep[current_guard] += int((ts - start_asleep).total_seconds() / 60)

            for m in range(start_asleep.minute, ts.minute):
                most_asleep[current_guard][m] += 1
            continue

    return total_sleep, most_asleep


def most_asleep(sleep_records):
    total_sleep, most_asleep = create_usable_data(sleep_records)
    result = sorted(((k, v) for k, v in total_sleep.items()), key=itemgetter(1), reverse=True)
    result = [(k, v, max(most_asleep[k].items(), key=itemgetter(1))[0]) for k, v in result]

    return result


def most_asleep_of_all(sleep_records):
    _, most_asleep = create_usable_data(sleep_records)

    by_minutes = [(g, m, dur) for g, dic in most_asleep.items() for m, dur in dic.items()]
    return max(by_minutes, key=itemgetter(2))[:2]


def test_most_asleep():
    assert most_asleep(parse_sleep_records(input_test)) == [
        (10, 50, 24),
        (99, 30, 45),
    ]


def test_most_asleep_of_all():
    assert most_asleep_of_all(parse_sleep_records(input_test)) == (99, 45)


if __name__ == '__main__':
    records = parse_sleep_records(open('input.txt').read())

    print('most_asleep:', reduce(mul, next(map(itemgetter(0, 2), most_asleep(records))), 1))
    print('most_asleep_of_all:', reduce(mul, most_asleep_of_all(records), 1))
