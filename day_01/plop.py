with open('input.txt') as f:
    input_ = [int(n) for n in f.read().split('\n') if n]


assert len(input_) == 200


for i in input_:
    for j in input_:
        if i + j == 2020:
            print(i * j)
