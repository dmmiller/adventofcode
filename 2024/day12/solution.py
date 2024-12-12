data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

with open("input.txt") as f:
  data = f.read()

type Point = tuple[int, int]

grid : list[str] = data.splitlines()
height = len(grid)
width = len(grid[0])

visited : set[Point] = set()
areas : dict[str, set[Point]] = {}
perimeters: dict[str, int] = {}

for y in range(height):
  for x in range(width):
    if (y, x) in visited:
      continue
    cell = grid[y][x]
    name = cell
    while name in areas:
      name = name + cell
    areas[name] = set()
    perimeters[name] = 0
    toConsider : list[Point] = [(y , x)]
    while len(toConsider) > 0:
      point = toConsider.pop(0)
      if point in visited:
        continue
      if grid[point[0]][point[1]] == cell:
        visited.add(point)
        areas[name].add(point)
      for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        newPoint = (point[0] + offset[0], point[1] + offset[1])
        if 0 <= newPoint[0] <  height and 0 <= newPoint[1] < width and grid[newPoint[0]][newPoint[1]] == cell and newPoint not in visited:
          toConsider.append(newPoint)
        if newPoint[0] < 0 or newPoint[0] >= height or newPoint[1] < 0 or newPoint[1] >= width or grid[newPoint[0]][newPoint[1]] != cell:
          perimeters[name] += 1


# for k in areas.keys():
#   print("region ", k, " has area ", len(areas[k]), " and perimeter ", perimeters[k])

print("Part 1 solution is ", sum(len(v) * perimeters[k] for k, v in areas.items()))