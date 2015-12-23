from functools import reduce
from itertools import product
from operator import mul

inp = '''Sprinkles: capacity 5, durability -1, flavor 0, texture 0, calories 5
PeanutButter: capacity -1, durability 3, flavor 0, texture 0, calories 1
Frosting: capacity 0, durability -1, flavor 4, texture 0, calories 6
Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8'''.split('\n')

ATTRIBUTES = ['capacity', 'durability', 'flavor', 'texture']
ingredients = {}

TOTAL_TEASPOONS = 100


def score(recipe, target_calories=0):
    if sum(recipe.values()) != TOTAL_TEASPOONS:
        return 0

    scores = {}
    for item in recipe.keys():
        for attr in ATTRIBUTES:
            scores[attr] = scores.get(attr, 0) + recipe[item] * ingredients.get(item)[attr]

    for item in scores.keys():
        scores[item] = max(0, scores[item])

    if target_calories != 0:
        calories = 0
        for item in recipe.keys():
            calories += recipe[item] * ingredients.get(item)['calories']
        if calories != target_calories:
            return 0

    return reduce(mul, scores.values())


for line in inp:
    line = line.replace(',', '')
    line = line.replace(':', '')
    line = line.split()

    ingredients[line[0]] = dict(zip(line[1::2], map(int, line[2::2])))

scores = []

for amounts in product(range(TOTAL_TEASPOONS), repeat=len(ingredients.keys())):
    if sum(amounts) != TOTAL_TEASPOONS:
        continue
    recipe = dict(zip(ingredients.keys(), amounts))
    scores.append((score(recipe, target_calories=500), recipe))

print(sorted(scores, key=lambda x: x[0], reverse=True)[:5])


# print(score({'Sprinkles':25, 'PeanutButter': 25, 'Frosting': 25, 'Sugar': 25}))
