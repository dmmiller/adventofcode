from __future__ import annotations
from collections import Counter
import re

FOOD_RE = re.compile(r"(?P<ingredients>.*) \(contains (?P<allergens>.*)\)")

def get_ingredients_and_allergens(line: str) -> tuple[set[str], set[str]]:
    match = FOOD_RE.match(line)
    ingredients = set(ingredient for ingredient in match['ingredients'].split(' '))
    allergens = set(allergen for allergen in match['allergens'].split(', '))
    return (ingredients, allergens)

def produce_allergen_list(allergen_map: dict[str, set[str]]) -> str:
    unique_allergen_map = determine_unique_allergens(allergen_map)
    return ','.join(unique_allergen_map[key] for key in sorted(unique_allergen_map.keys()))

def determine_unique_allergens(allergen_map: dict[str, set[str]]) -> dict[str, str]:
    unique_allergen_map = {}
    while len(unique_allergen_map) != len(allergen_map):
        for allergen, possible_ingredients in allergen_map.items():
            if allergen in unique_allergen_map:
                continue
            remaining_possible_ingredients = [ingredient for ingredient in possible_ingredients if ingredient not in unique_allergen_map.values()]
            if len(remaining_possible_ingredients) == 1:
                unique_allergen_map[allergen] = remaining_possible_ingredients[0]
    return unique_allergen_map
    
ingredients_count = Counter()
allergen_map = {}

with open('input.txt') as f:
    for line in f.readlines():
        ingredients, allergens = get_ingredients_and_allergens(line.strip())
        ingredients_count.update(ingredients)
        for allergen in allergens:
            if allergen not in allergen_map:
                allergen_map[allergen] = set(ingredients)
            allergen_map[allergen] &= ingredients
    possible_allergens = set.union(*allergen_map.values())
    total_impossible_ingredients = sum(v for k, v in ingredients_count.items() if k not in possible_allergens)
    print(f"The total number of ingredients which can't contain allergens is {total_impossible_ingredients}")
    print(f"The dangerous ingredient list is {produce_allergen_list(allergen_map)}")