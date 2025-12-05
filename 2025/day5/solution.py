data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

with open("input.txt") as f:
  data = f.read()

rawRanges, rawIngredients = data.split("\n\n")

ranges = [[min(int(parts[0]), int(parts[1])), max(int(parts[0]), int(parts[1]))] for line in rawRanges.splitlines() if (parts := line.split("-"))]
ingredients = [int(line) for line in rawIngredients.splitlines()]

part1Solution = 0
for ingredient in ingredients:
  for r in ranges:
    if r[0] <= ingredient <= r[1]:
      part1Solution += 1
      break

print("Part 1 solution is ", part1Solution)

ranges = sorted(ranges, key=lambda a: (a[0], a[1]))

mergedRanges = []
currentRange = ranges[0]

for i in range(1, len(ranges)):
  nextRange = ranges[i]
  if nextRange[0] <= currentRange[1] <= nextRange[1] or (nextRange[0] >= currentRange[0] and nextRange[1] <= currentRange[1]):
    currentRange = [min(currentRange[0], nextRange[0]), max(currentRange[1], nextRange[1])]
  else:
    mergedRanges.append(currentRange)
    currentRange = nextRange
mergedRanges.append(currentRange)

part2Solution = sum(r[1] - r[0] + 1 for r in mergedRanges)
print("Part 2 solution is ", part2Solution)