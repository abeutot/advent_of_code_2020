passes = [l.strip().split() for l in open('input.txt')]
passes = [([int(i) for i in a.split('-')], b[0], c) for a,b,c in passes]

print(sum(1 for ((min_, max_), letter, p) in passes
          if min_ <= p.count(letter) <= max_))
