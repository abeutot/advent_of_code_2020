import itertools
from functools import reduce
from operator import itemgetter, or_, and_
from collections import defaultdict
from pprint import pprint


def parse(input_):
    list_of_foods = [l.rstrip(')').split(' (contains ') for l in input_.rstrip('\n').split('\n')]
    list_of_foods = [(set(a.split(' ')), set(b.split(', '))) for a, b in list_of_foods]

    return list_of_foods


def get_allergens(list_of_foods):
    allergen_candidates = defaultdict(list)
    for ingredients, allergens in list_of_foods:
        for a in allergens:
            allergen_candidates[a].append(ingredients)
    # turn into a regular dict
    allergen_candidates = {k: v for k, v in allergen_candidates.items()}

    allergens = {}
    # print('candidates:')
    # pprint(allergen_candidates)
    # print('allergens:')
    # pprint(allergens)
    while allergen_candidates:
        for a, ingredients in allergen_candidates.items():
            current_allergens = allergens.get(a, set())

            # corner case where our combination method is not working
            if len(ingredients) == 1 and len(ingredients[0]) == 1:
                current_allergens.add(ingredients[0].pop())

            # try every possible intersection combinations between the
            # different ingredients lists to see if we can isolate one
            for i in range(2, len(ingredients) + 1):
                for intersection in itertools.combinations(ingredients, i):
                    intersection = reduce(and_, intersection)
                    if len(intersection) == 1:
                        current_allergens.add(intersection.pop())

            if current_allergens:
                allergens[a] = current_allergens

        # remove elected allergens from its own candidate set
        allergen_candidates = {a: [i
                                   for i in ingredients
                                   if a not in allergens or not (allergens[a] & i)]
                               for a, ingredients in allergen_candidates.items()}
        # remove empty allergens candidates
        allergen_candidates = {a: i for a, i in allergen_candidates.items()
                               if i and (len(i) != 1 or len(i[0]) != 0)}

        # remove elected allergens from other candidates
        allergen_candidates = {a: [i - other_canditates for i in ingredients]
                               for a, ingredients, other_canditates in map(
                                   lambda t: (
                                       *t,
                                       reduce(
                                           or_,
                                           (ii for aa, ii in allergens.items()
                                            if aa != a),
                                           set(),
                                       ),
                                   ),
                                   allergen_candidates.items(),
                               )}

        # print(len(allergen_candidates))
        # print('candidates:')
        # pprint(allergen_candidates)
        # print('allergens:')
        # pprint(allergens)

    return allergens


def part1(list_of_foods):
    allergens = get_allergens(list_of_foods)

    all_ingredients = set(itertools.chain.from_iterable(map(itemgetter(0), list_of_foods)))
    all_allergen_ingredients = reduce(or_, allergens.values())
    non_allergen_ingredients = all_ingredients - all_allergen_ingredients

    return sum(1
               for i in itertools.chain.from_iterable(map(itemgetter(0), list_of_foods))
               if i in non_allergen_ingredients)


input_test = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
def test_part1():
    assert part1(parse(input_test)) == 5


def part2(list_of_foods):
    allergens = get_allergens(list_of_foods)

    for a, i in allergens.items():
        assert len(i) == 1

    allergens = [(a, i.pop()) for a, i in allergens.items()]

    # print('allergens:', allergens)

    return ','.join(map(itemgetter(1), sorted(allergens, key=itemgetter(0))))


def test_part2():
    assert part2(parse(input_test)) == 'mxmxvkd,sqjhc,fvjkl'


if __name__ == '__main__':
    input_ = parse(open('input.txt').read())
    print('part1:', part1(input_))
    print('part2:', part2(input_))
