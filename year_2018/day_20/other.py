import networkx

maze = networkx.Graph()

paths = open('input.txt').read()[1:-1]

pos = {0}  # the current positions that we're building on
stack = []  # a stack keeping track of (starts, ends) for groups
starts, ends = {0}, set()  # current possible starting and ending positions

for c in paths:
    if c == '|':
        # an alternate: update possible ending points, and restart the group
        ends.update(pos)
        pos = starts
    elif c in 'NESW':
        # move in a given direction: add all edges and update our current positions
        direction = {'N': 1, 'E': 1j, 'S': -1, 'W': -1j}[c]
        maze.add_edges_from((p, p + direction) for p in pos)
        pos = {p + direction for p in pos}
    elif c == '(':
        # start of group: add current positions as start of a new group
        stack.append((starts, ends))
        starts, ends = pos, set()
    elif c == ')':
        # end of group: finish current group, add current positions as possible ends
        pos.update(ends)
        starts, ends = stack.pop()

# find the shortest path lengths from the starting room to all other rooms
lengths = networkx.algorithms.shortest_path_length(maze, 0)

print('part1:', max(lengths.values()))
# print('part2:', sum(1 for length in lengths.values() if length >= 1000))
