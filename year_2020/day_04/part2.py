import re
import sys
from operator import itemgetter

passports = open(sys.argv[1]).read().split('\n\n')

mandatory_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}  # , 'cid'}

passports = [[f.split(':') for f in p.split()] for p in passports]

def validate_field(f):
    n, v = f

    if n == 'byr':
        if len(v) != 4:
            return False
        return '1920' <= v <= '2002'

    if n == 'iyr':
        if len(v) != 4:
            return False
        return '2010' <= v <= '2020'

    if n == 'eyr':
        if len(v) != 4:
            return False
        return '2020' <= v <= '2030'

    if n == 'hgt':
        if v.endswith('cm'):
            if len(v) != 5:
                return False
            return '150' <= v[:3] <= '193'

        if v.endswith('in'):
            if len(v) != 4:
                return False
            return '59' <= v[:2] <= '76'

        return False

    if n == 'hcl':
        return bool(re.match(r'^#[0-9a-f]{6}$', v))

    if n == 'ecl':
        return v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    if n == 'pid':
        return v.isdigit() and len(v) == 9

    if n == 'cid':
        return True

    return False


valid = sum(1 for p in passports
            if mandatory_fields <= set(map(itemgetter(0), (f for f in p)))
               and sum(map(validate_field, p)) == len(p))

print(valid)
