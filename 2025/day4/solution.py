data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

with open("input.txt") as f:
  data = f.read()

grid = set()

row = 0
columnWidth = 0
rowHeight = 0
for line in data.splitlines():
  columnWidth = len(line)
  for c in range(len(line)):
    if line[c] == '@':
      grid.add((row, c))
  row = row + 1

rowHeight = row

def surroundingCount(x: int, y: int) -> int:
  count = 0
  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == j and i == 0:
        continue
      if (x + i, y + j) in grid:
        count += 1
  return count

part1Solution = sum(1 if (x,y) in grid and surroundingCount(x,y) < 4 else 0 for x in range(rowHeight) for y in range(columnWidth))
print('Part 1 solution is ', part1Solution)

part2Solution = 0
removed = True
while removed:
  removed = False
  for x in range(rowHeight):
    for y in range(columnWidth):
      if (x, y) in grid:
        neighbours = surroundingCount(x,y)
        if neighbours < 4:
          part2Solution += 1
          grid.remove((x,y))
          removed = True

print("Part 2 solution is ", part2Solution)