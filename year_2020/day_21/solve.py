#!/usr/bin/env python
import re
import sys
from collections import Counter, namedtuple
from itertools import chain
from typing import Dict, List, Set, Tuple


Food = namedtuple('Food', ('ingredients', 'allergens'))


def parse(filename: str) -> List[Food]:
    foods = []
    with open(filename) as f:
        for line in f.readlines():
            m = re.match(r'(.*?)\(contains (.*?)\)', line)
            assert m
            foods.append(Food(m[1].split(), m[2].split(', ')))

    return foods


def get_ingredients(foods: List[Food]) -> Tuple[Set[str], Dict[str, str]]:
    contained = {}
    ingredients = set()
    for food in foods:
        ingredients |= set(food.ingredients)
        for allergen in food.allergens:
            if allergen not in contained:
                contained[allergen] = set(food.ingredients)
            else:
                contained[allergen] &= set(food.ingredients)

    changes = True
    while changes:
        changes = False
        guessed = set(chain(*(a for i, a in contained.items() if len(a) == 1)))
        for i, a in contained.items():
            if len(a) != 1:
                contained[i] = a - guessed
                changes = True

    safe_ingredients = ingredients - set(chain(*contained.values()))
    return safe_ingredients, {i: a.pop() for i, a in contained.items()}


def main(filename: str) -> None:
    foods = parse(filename)
    safe_ingredients, unsafe_ingredients = get_ingredients(foods)
    safe_count = sum(Counter(
        ingredient
        for ingredient in chain(*(food.ingredients for food in foods))
        if ingredient in safe_ingredients
    ).values())
    print(f'Step 1: {safe_count}')

    allergens = [a for i, a in sorted(unsafe_ingredients.items())]
    print(f'Step 2: {",".join(allergens)}')


if __name__ == '__main__':
    main(sys.argv[1])
