from collections import defaultdict
from typing import Callable, Counter

data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

with open("input.txt") as f:
    data = f.read()

template, pairs = data.split("\n\n")
rules = {}
for pair in pairs.split("\n"):
    rules[pair[:2]] = pair[6]

def part1(template, steps):
    for step in range(steps):
        next = ""
        for i in range(len(template)-1):
            next += template[i] + rules[template[i:i+2]]
        next += template[-1]
        template = next
    element_count = Counter(template)
    max_value = max(element_count.values())
    min_value = min(element_count.values())
    return max_value - min_value

print(f"Part 1 Max count - min count = {part1(template, 10)}")


# part2 is just more iterations so we have to be smarter rather than just looping all iterations
rules2 = {k : [k[0] + v, v + k[1]] for k,v in rules.items()}

def part2(template, steps):
    element_pairs = Counter(template[i:i+2] for i in range(len(template) - 1))
    start = template[0:2]
    for i in range(40):
        next = defaultdict(int)
        for pair, count in element_pairs.items():
            next[rules2[pair][0]] += count
            next[rules2[pair][1]] += count
        start = rules2[start][0]
        element_pairs = next
    final_count = defaultdict(int)
    for k, v in element_pairs.items():
        final_count[k[1]] += v
    final_count[start[0]] += 1
    max_value = max(final_count.values())
    min_value = min(final_count.values())
    return max_value - min_value

print(f"Part 2 Max count - min count = {part2(template, 40)}")