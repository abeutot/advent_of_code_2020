passes = [l.strip().split() for l in open('input.txt')]
passes = [([int(i) for i in a.split('-')], b[0], c) for a,b,c in passes]

count = 0
for ((pos1, pos2), letter, p) in passes:
    try:
        if (p[pos1 - 1] == letter) != (p[pos2 - 1] == letter):
            count += 1
    except:
        print(pos1, pos2, letter, p)
        raise

print(count)
