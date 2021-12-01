import string
import itertools
from collections import defaultdict


input_test = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""



def order_of_execution(input_):
    dependencies = defaultdict(set)

    for i in input_.rstrip('\n').split('\n'):
        dependency, step = i[5], i[36]
        # print('dep:', dependency, 'step:', step)
        dependencies[dependency]  # make sure every node exists as key
        dependencies[step].add(dependency)

    order = []
    while dependencies:
        # print('dependencies:', dependencies, 'order:', order)
        can_begin, *_ = sorted({s for s, d in dependencies.items() if not d})
        order.append(can_begin)

        dependencies = {k: v - {can_begin} for k, v in dependencies.items() if k != can_begin}

    return ''.join(order)


def test_order_of_execution():
    assert order_of_execution(input_test) == 'CABDFE'


def time_to_complete(input_, step_duration, worker_count):
    dependencies = defaultdict(set)
    durations = {l: step_duration + i + 1 for i, l in enumerate(string.ascii_uppercase)}
    in_progress = set()

    for i in input_.rstrip('\n').split('\n'):
        dependency, step = i[5], i[36]
        # print('dep:', dependency, 'step:', step)
        dependencies[dependency]  # make sure every node exists as key
        dependencies[step].add(dependency)

    for t in itertools.count():
        if not dependencies:
            break

        done = {s for s in in_progress if durations[s] == 0}
        in_progress = {s for s in in_progress if durations[s] > 0}

        dependencies = {k: v - done for k, v in dependencies.items() if k not in done}

        # print('time:', t)
        # print('dependencies:', dependencies)
        # print('in_progress:', in_progress)
        # print('done:', done)

        can_begin = sorted({s for s, d in dependencies.items() if not d and s not in in_progress})

        # print('can_begin:', can_begin)

        while can_begin and len(in_progress) < worker_count:
            c, *can_begin = can_begin
            in_progress.add(c)

        for s in in_progress:
            durations[s] -= 1

    return t - 1


def test_time():
    assert time_to_complete(input_test, 0, 2) == 15


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('order:', order_of_execution(input_))
    print('time:', time_to_complete(input_, 60, 5))
