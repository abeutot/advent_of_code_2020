import sys
from operator import itemgetter

passports = open(sys.argv[1]).read().split('\n\n')

mandatory_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}  # , 'cid'}

passports = [[f.split(':') for f in p.split()] for p in passports]

valid = sum(1 for p in passports if mandatory_fields <= set(map(itemgetter(0), (f for f in p))))

print(valid)
