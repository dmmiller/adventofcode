data = """0123
1234
8765
9876"""

data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

with open("input.txt") as f:
  data = f.read()

type Point = tuple[int, int]
grid : list[str] = data.splitlines()
# Part 1 counts how many reachable 9s there are
pointToReachableMap : dict[Point, set[Point]] = {}
# Part 2 counts how many paths to those 9 there are
pointToPathCountMap : dict[Point, int] = {}

height = len(grid)
width = len(grid[0])
for y in range(height):
  for x in range(width):
    val = int(grid[y][x])
    point = (y, x)
    pointToReachableMap[point] = set([point]) if val == 9 else set()
    pointToPathCountMap[point] = 1 if val == 9 else 0

for value in range (8, -1, -1):
  for y in range(height):
    for x in range(width):
      if int(grid[y][x]) != value:
        continue
      point = (y, x)
      if 0 <= y - 1 and int(grid[y - 1][x]) == value + 1:
        pointToReachableMap[point] |= pointToReachableMap[(y - 1, x)]
        pointToPathCountMap[point] += pointToPathCountMap[(y - 1, x)]
      if x + 1 < width and int(grid[y][x + 1]) == value + 1:
        pointToReachableMap[point] |= pointToReachableMap[(y, x + 1)]
        pointToPathCountMap[point] += pointToPathCountMap[(y, x + 1)]
      if y + 1 < height and int(grid[y + 1][x]) == value + 1:
        pointToReachableMap[point] |= pointToReachableMap[(y + 1, x)]
        pointToPathCountMap[point] += pointToPathCountMap[(y + 1, x)]
      if 0 <= x - 1 and int(grid[y][x - 1]) == value + 1:
        pointToReachableMap[point] |= pointToReachableMap[(y, x - 1)]
        pointToPathCountMap[point] += pointToPathCountMap[(y, x - 1)]

part1Total = 0
part2Total = 0
for y in range(height):
  for x in range(width):
    if grid[y][x] == '0':
      part1Total += len(pointToReachableMap[(y, x)])
      part2Total += pointToPathCountMap[(y, x)]

print("Part 1 solution is ", part1Total)
print("Part 2 solution is ", part2Total)