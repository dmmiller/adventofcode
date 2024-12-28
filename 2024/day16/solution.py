from collections import deque

data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

with open("input.txt") as f:
  data = f.read()

type Point = tuple[int, int]

# x offset, y offset
type Direction = tuple[int, int]

def buildMaze(rows: list[str]) -> tuple[set[Point], Point, Point]:
  start: Point = (0, 0)
  end: Point = (0, 0)
  walls: set[Point] = set()
  height = len(rows)
  width = len(rows[0])
  for y in range(height):
    for x in range(width):
      point = (x, y)
      value = rows[y][x]
      if value == "#":
        walls.add(point)
      elif value == "S":
        start = point
      elif value == "E":
        end = point

  return (walls, start, end)


def printMaze(walls, start, end):
  height = max(wall[1] for wall in walls) + 1
  width = max(wall[0] for wall in walls) + 1
  for y in range(height):
    for x in range(width):
      point = (x, y)
      if point in walls:
        print("#", end="")
      elif point == start:
        print("S", end="")
      elif point == end:
        print("E", end="")
      else:
        print(".", end="")
    print("")
  print("")

def findCostAndSeats(start: Point, end: Point, walls: set[Point]) -> tuple[int, set[Point]]:
  costs: dict[tuple[Point, Direction], int] = {}
  costs[(start, (1, 0))] = 0
  seatPaths: dict[tuple[Point, Direction], set[Point]] = {}
  seatPaths[(start, (1, 0))] = set()

  toVisit: deque[tuple[Point, Direction]] = deque()
  toVisit.append((start, (1, 0)))

  while len(toVisit) > 0:
    point, direction = toVisit.popleft()
    minCost = costs[(point, direction)]
    seatsSoFar = seatPaths[(point, direction)]
    seatsSoFar.add(point)
    for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
      newPoint: Point = (point[0] + offset[0], point[1] + offset[1])
      if newPoint not in walls:
        newCost = minCost + 1
        if direction != offset and (direction[0] == offset[0] or direction[1] == offset[1]):
          newCost += 2000
        elif direction != offset:
          newCost += 1000
        if (newPoint, offset) not in costs or costs[(newPoint, offset)] >= newCost:
          if (newPoint, offset) in costs and costs[(newPoint, offset)] == newCost:
            # merge paths so far
            seatPaths[(newPoint, offset)] = seatPaths[(newPoint, offset)].union(seatsSoFar)
            continue
          toVisit.append((newPoint, offset))
          costs[(newPoint, offset)] = newCost
          seatPaths[(newPoint, offset)] = set(seatsSoFar)

  maxCost = max(value for value in costs.values())
  minCost =  min(value if key[0] == end else maxCost for key, value in costs.items())
  seats = set()
  for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    if (end, offset) in costs and costs[(end, offset)] == minCost:
      seats = seats.union(seatPaths[end, offset])
  return (minCost, seats)


walls, start, end = buildMaze(data.splitlines())
cost, seats = findCostAndSeats(start, end, walls)
print("Part 1 solution is ", cost)
print("Part 2 solution is ", len(seats))