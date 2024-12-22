data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

with open("input.txt") as f:
  data = f.read()

type Point = tuple[int, int]


def buildMaze(maze: list[str]) -> tuple[set[Point], dict[Point, int], Point, Point]:
  walls : set[Point] = set()
  path: dict[Point, int] = {}
  start : Point = (0,0)
  end : Point = (0, 0)
  height = len(maze)
  width = len(maze[0])

  for y in range(height):
    for x in range(width):
      cell = maze[y][x]
      if cell == "#":
        walls.add((x, y))
      elif cell == "S":
        start = (x, y)
      elif cell == "E":
        end = (x, y)

  cost = 0
  point = start
  while point != end:
    path[point] = cost
    cost += 1
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      newPoint = (point[0] + offset[0], point[1] + offset[1])
      if 0 <= newPoint[0] < width and 0 <= newPoint[1] < height and newPoint not in walls and newPoint not in path:
        point = newPoint
        break

  path[end] = cost
  return (walls, path, start, end)


def countCheats(walls: set[Point], pathMap: dict[Point, int], threshold: int) -> int:
  sortedPath : list[Point ]= sorted(pathMap, key=lambda x: pathMap[x])
  totalCheats = 0
  for point in sortedPath:
    value = pathMap[point]
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      adjacentPoint = (point[0] + offset[0], point[1] + offset[1])
      if adjacentPoint in walls:
        doublePoint = (adjacentPoint[0] + offset[0], adjacentPoint[1] + offset[1])
        if doublePoint in pathMap and value + 2 < pathMap[doublePoint] and pathMap[doublePoint] - (value + 2) >= threshold:
          totalCheats += 1
  return totalCheats

walls, pathMap, start, end = buildMaze(data.splitlines())

print("Part 1 solution is ", countCheats(walls, pathMap, 100))