map_ = [l for l in open('input.txt').read().split('\n') if l]

mul = 1
for i, j in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    x, y = 0, 0
    tree_count = 0
    empty_count = 0

    while y + j < len(map_):
        x += i
        y += j

        if map_[y][x % len(map_[y])] == '#':
            tree_count += 1
        else:
            empty_count += 1

    mul *= tree_count

    print('i: ', i, 'j: ', j, 'tree: ', tree_count, 'empty: ', empty_count)

print('mul: ', mul)
