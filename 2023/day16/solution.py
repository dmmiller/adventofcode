from enum import Enum
from collections import deque

data = """.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|...."""

with open("input.txt") as f:
  data = f.read()

mirrors: dict[tuple[int, int], str] = dict(
    [[(x, y), c] for y, row in enumerate(data.splitlines())
     for x, c in enumerate(row) if c != "."])

xBound = len(data.splitlines()[0])
yBound = len(data.splitlines())

Direction = Enum('Direction', ['N', 'E', 'S', 'W'])


def getDirections(current: Direction, x: int, y: int) -> list[Direction]:
  if (x, y) not in mirrors:
    return [current]

  mirror = mirrors[(x, y)]
  if mirror == "|":
    if current == Direction.N or current == Direction.S:
      return [current]
    else:
      return [Direction.N, Direction.S]
  if mirror == "-":
    if current == Direction.E or current == Direction.W:
      return [current]
    else:
      return [Direction.E, Direction.W]
  if mirror == "/":
    if current == Direction.N:
      return [Direction.E]
    if current == Direction.E:
      return [Direction.N]
    if current == Direction.S:
      return [Direction.W]
    if current == Direction.W:
      return [Direction.S]
  if mirror == "\\":
    if current == Direction.N:
      return [Direction.W]
    if current == Direction.E:
      return [Direction.S]
    if current == Direction.S:
      return [Direction.E]
    if current == Direction.W:
      return [Direction.N]


def countEnergized(x: int, y: int, startDirection: Direction) -> int:
  seen: set[tuple[int, int, Direction]] = set()
  edges: deque[tuple[int, int, Direction]] = deque()
  edges.append((x, y, startDirection))

  while len(edges):
    edge = edges.popleft()
    if edge in seen:
      continue
    nextDirections = getDirections(edge[2], edge[0], edge[1])
    for direction in nextDirections:
      nextEdge = (edge[0], edge[1], direction)
      if direction == Direction.N:
        nextEdge = (edge[0], edge[1] - 1, direction)
      if direction == Direction.E:
        nextEdge = (edge[0] + 1, edge[1], direction)
      if direction == Direction.S:
        nextEdge = (edge[0], edge[1] + 1, direction)
      if direction == Direction.W:
        nextEdge = (edge[0] - 1, edge[1], direction)
      if 0 <= nextEdge[0] < xBound and 0 <= nextEdge[1] < yBound:
        edges.append(nextEdge)
    seen.add(edge)

  board = dict(map(lambda v: [(v[0], v[1]), 1], seen))
  return len(board)


print("Part 1 solution : ", countEnergized(0, 0, Direction.E))
part2Max = 0
for x in range(xBound):
  top = countEnergized(x, 0, Direction.S)
  bottom = countEnergized(x, yBound - 1, Direction.N)
  if max(top, bottom) > part2Max:
    part2Max = max(top, bottom)

for y in range(yBound):
  left = countEnergized(0, y, Direction.E)
  right = countEnergized(xBound - 1, y, Direction.W)
  if max(left, right) > part2Max:
    part2Max = max(left, right)

print("Part 2 solution : ", part2Max)
