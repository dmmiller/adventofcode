from collections import Counter
from typing import Iterable

def compute_gaps(numbers : Iterable[int]) -> Counter:
    previous = 0 #outlet joltage
    gaps = Counter()
    for num in sorted(numbers):
        gaps[num - previous] += 1
        previous = num
    # add one more gap 3 for the final jump
    gaps[3] += 1
    return gaps

def count_arrangements(numbers : Iterable[int]) -> int:
    target = max(numbers)
    counter = Counter()
    counter[0] = 1
    for i in range(1, target+1):
        if i in numbers:
            counter[i] = counter[i - 1] + counter[i - 2] + counter[i-3]
    return counter[target]

with open('input.txt') as f:
    numbers = [int(line.strip()) for line in f]
gap_counter = compute_gaps(numbers)
print(f"Product of 1 and 3 gaps is {gap_counter[1] * gap_counter[3]}")
print(f"Number of ways to get there is {count_arrangements(numbers)}")