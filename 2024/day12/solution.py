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

print("Part 1 solution is ", sum(len(v) * perimeters[k] for k, v in areas.items()))

def sideCount(points: set[Point]) -> int:
  miny = min(points, key=lambda p: p[0])[0]
  maxy = max(points, key=lambda p: p[0])[0]
  minx = min(points, key=lambda p: p[1])[1]
  maxx = max(points, key=lambda p: p[1])[1]
  count = 0
  for y in range (miny, maxy + 2):
    growingSide = False
    for x in range(minx, maxx + 1):
      isAboveInPoints = (y - 1, x) in points
      isLeftinPoints = (y, x - 1) in points
      if (y, x) in points:
        if growingSide and isAboveInPoints:
          growingSide = False
        elif growingSide and not isAboveInPoints:
          if not isLeftinPoints:
            count += 1
        elif not growingSide and isAboveInPoints:
          pass
        elif not growingSide and not isAboveInPoints:
          growingSide = True
          count += 1
      else:
        if growingSide and isAboveInPoints:
          if isLeftinPoints:
            count += 1
        elif growingSide and not isAboveInPoints:
          growingSide = False
        elif not growingSide and isAboveInPoints:
          growingSide = True
          count += 1
        elif not growingSide and not isAboveInPoints:
          pass

  for x in range(minx, maxx + 2):
    growingSide = False
    for y in range (miny, maxy + 1):
      isLeftInPoints = (y, x - 1) in points
      isAboveInPoints = (y - 1, x) in points
      if (y, x) in points:
        if growingSide and isLeftInPoints:
          growingSide = False
        elif growingSide and not isLeftInPoints:
          if not isAboveInPoints:
            count += 1
        elif not growingSide and isLeftInPoints:
          pass
        elif not growingSide and not isLeftInPoints:
          growingSide = True
          count += 1
      else:
        if growingSide and isLeftInPoints:
          if isAboveInPoints:
            count += 1
        elif growingSide and not isLeftInPoints:
          growingSide = False
        elif not growingSide and isLeftInPoints:
          growingSide = True
          count += 1
        elif not growingSide and not isLeftInPoints:
          pass

  return count

# for k, v in areas.items():
#   print("region ", k, " has area ", len(v), " and side count ", sideCount(v))

print("Part 2 solution is ", sum(len(v) * sideCount(v) for v in areas.values()))