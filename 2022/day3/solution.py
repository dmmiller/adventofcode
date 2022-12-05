from functools import reduce

# data = """vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw"""

with open("input.txt") as f:
    data = f.read()


def buildRucksack(s: str):
    mid = int(len(s) / 2)
    return set(s[:mid]), set(s[mid:])


def score(s: set):
    element = s.pop()
    value = 0
    if element.isupper():
        value = ord(element) - ord('A') + 27
    else:
        value = ord(element) - ord('a') + 1
    return value


rucksacks = [buildRucksack(line) for line in data.splitlines()]
intersections = [left & right for left, right in rucksacks]
print(f"Part 1 priorities sum is {sum(score(i) for i in intersections)}")

full_rucksack = [left | right for left, right in rucksacks]

common = [reduce(lambda x, y: x & y, full_rucksack[i * 3: i * 3 + 3])
          for i in range(int(len(full_rucksack) / 3))]
print(f"Part 2 priorites sum is {sum(score(e) for e in common)}")
