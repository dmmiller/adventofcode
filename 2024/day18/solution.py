import heapq

data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

type Point = tuple[int, int]
target: Point = (6, 6)
byteCount = 12

with open("input.txt") as f:
  data = f.read()
target: Point = (70, 70)
byteCount = 1024

points: list[Point] = [(int(point[0]), int(point[1])) for line in data.splitlines() if len(point := line.split(",")) == 2]

def findShortestPathLength(bytes: set[Point], target: Point) -> int:
  point: Point = (0, 0)
  distanceMap: dict[Point, int] = {(0, 0) : 0}

  unexplored: list[Point] = [point]
  while len(unexplored):
    point = unexplored.pop(0)
    base = distanceMap[point]
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
      newPoint = (point[0] + offset[0], point[1] + offset[1])
      if newPoint not in bytes and 0 <= newPoint[0] <= target[0] and 0 <= newPoint[1] <= target[1]:
        if newPoint not in distanceMap or base + 1 < distanceMap[newPoint]:
          distanceMap[newPoint] = base + 1
          unexplored.append(newPoint)

  return distanceMap[target]

print("Part 1 solution is ", findShortestPathLength(set(points[:byteCount]), target))

def findBlockingPath(byteList: list[Point], target: Point) -> Point:

  def isBlocked(i: int) -> bool:
    point: Point = (0, 0)
    distanceMap: dict[Point, int] = {(0, 0) : 0}
    bytes = set(byteList[:i])

    unexplored: list[Point] = [point]
    while len(unexplored):
      point = unexplored.pop(0)
      base = distanceMap[point]
      for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        newPoint = (point[0] + offset[0], point[1] + offset[1])
        if newPoint not in bytes and 0 <= newPoint[0] <= target[0] and 0 <= newPoint[1] <= target[1]:
          if newPoint not in distanceMap or base + 1 < distanceMap[newPoint]:
            distanceMap[newPoint] = base + 1
            unexplored.append(newPoint)

    return target not in distanceMap

  def bisect(left: int, right: int) -> int:
    if left == right or left + 1 == right:
      return left
    mid = (left + right) // 2
    if isBlocked(mid):
      return bisect(left, mid)
    else:
      return bisect(mid, right)

  index =  bisect(0, len(byteList))
  return byteList[index]

print("Part 2 solution is ", findBlockingPath(points, target))