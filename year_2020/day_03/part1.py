map_ = [l for l in open('input.txt').read().split('\n') if l][1:]

pos = 3
count = 0
other_count = 0

for l in map_:
    if l[pos % len(l)] == '#':
        count += 1
    else:
        other_count += 1

    pos += 3

print(count, other_count)
