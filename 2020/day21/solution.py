from __future__ import annotations
from collections import Counter
import re

food_re = re.compile(r"(?P<ingredients>.*) \(contains (?P<allergens>.*)\)")

def get_ingredients_and_allergens(line: str) -> tuple[set[str], set[str]]:
    match = food_re.match(line)
    ingredients = set(ingredient.strip() for ingredient in match['ingredients'].split(' '))
    allergens = set(ingredient.strip() for ingredient in match['allergens'].split(','))
    return (ingredients, allergens)

def produce_allergen_list(allergen_map: dict[str, set[str]]) -> str:
    locked = {}
    while len(allergen_map) > 0:
        removed_item = ''
        for k, v in allergen_map.items():
            if len(v) == 1:
                removed_item = v.pop()
                locked[k] = removed_item
                del allergen_map[k]
                break
        for k, v in allergen_map.items():
            if removed_item in v:
                v.remove(removed_item)

    return ','.join(locked[key] for key in sorted(locked.keys()))
    
all_ingredients_counter = Counter()
allergen_map = {}

with open('input.txt') as f:
    for line in f.readlines():
        ingredients, allergens = get_ingredients_and_allergens(line.strip())
        all_ingredients_counter.update(ingredients)
        for allergen in allergens:
            if allergen not in allergen_map:
                allergen_map[allergen] = set(ingredients)
            allergen_map[allergen] = allergen_map[allergen].intersection(ingredients)
    possible_allergens = set(allergen for allergens in allergen_map.values() for allergen in allergens)
    total_impossible_ingredients = sum(v for k, v in all_ingredients_counter.items() if k not in possible_allergens)
    print(f"The total number of ingredients which can't contain allergens is {total_impossible_ingredients}")
    print(f"The dangerous ingredient list is {produce_allergen_list(allergen_map)}")