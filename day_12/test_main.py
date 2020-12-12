input_test = """F10
N3
F7
R90
F11"""


def distance(input_):
    instructions = [(l[0], int(l[1:])) for l in input_.rstrip('\n').split('\n')]

    directions = ('E', 'S', 'W', 'N')
    current_x, current_y = 0, 0
    facing_direction = 'E'

    for i, o in instructions:
        # print('pos:', current_x, current_y)
        if i == 'F':
            i = facing_direction

        if i == 'N':
            current_y += o
            continue
        if i == 'S':
            current_y -= o
            continue
        if i == 'E':
            current_x += o
            continue
        if i == 'W':
            current_x -= o
            continue

        if i == 'L':
            current_index = directions.index(facing_direction)
            facing_direction = directions[(current_index - (o // 90)) % len(directions)]
            continue
        if i == 'R':
            current_index = directions.index(facing_direction)
            facing_direction = directions[(current_index + (o // 90)) % len(directions)]
            continue
    # print('pos:', current_x, current_y)

    return abs(current_x) + abs(current_y)


def test_distance():
    assert distance(input_test) == 25


def distance_2(input_):
    instructions = [(l[0], int(l[1:])) for l in input_.rstrip('\n').split('\n')]

    directions = ('E', 'S', 'W', 'N')
    ship_x, ship_y = 0, 0
    waypoint_x, waypoint_y = 10, 1

    for i, o in instructions:
        if i == 'F':
            ship_x, ship_y = ship_x + waypoint_x * o, ship_y + waypoint_y * o
        elif i == 'N':
            waypoint_y += o
        elif i == 'S':
            waypoint_y -= o
        elif i == 'E':
            waypoint_x += o
        elif i == 'W':
            waypoint_x -= o
        elif i == 'L':
            for _ in range(o // 90):
                waypoint_x, waypoint_y = -waypoint_y, waypoint_x
        elif i == 'R':
            for _ in range(o // 90):
                waypoint_x, waypoint_y = waypoint_y, -waypoint_x

        # print('ship:', ship_x, ship_y, 'waypoint:', waypoint_x, waypoint_y)

    return abs(ship_x) + abs(ship_y)


def test_distance_2():
    assert distance_2(input_test) == 286


if __name__ == '__main__':
    input_ = open('input.txt').read()
    print('distance:', distance(input_))
    print('distance 2:', distance_2(input_))
