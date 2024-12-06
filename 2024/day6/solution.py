data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

with open("input.txt") as f:
  data = f.read()

grid :list[str] = data.splitlines()

# these are stored in (y, x) order
obstacles : set[tuple[int, int]] = set()
guard: tuple[int, int] = (0,0)

height = len(grid)
width = len(grid[0])
for y in range(height):
  for x in range(width):
    if grid[y][x] == "#":
      obstacles.add((y, x))
    elif grid[y][x] == "^":
      guard = (y, x)

visited : set[tuple[int, int]] = set()
direction : tuple[int, int] = (-1, 0)
originalGuard = guard

# Part 1
while 0 <= guard[0] < height and 0 <= guard[1] < width:
  visited.add(guard)
  newSquare = (guard[0] + direction[0], guard[1] + direction[1])
  if newSquare in obstacles:
    newSquare = guard
    if direction[0] == -1:
      direction = (0, 1)
    elif direction[1] == 1:
      direction = (1, 0)
    elif direction[0] == 1:
      direction = (0, -1)
    elif direction[1] == -1:
      direction = (-1, 0)
  guard = newSquare

# Part 2
obstructionPossibilities = 0
for possibility in visited:
  if possibility == originalGuard:
    continue

  obstacles.add(possibility)
  guard = originalGuard
  direction = (-1, 0)
  # need to track visited and direction
  localVisited : set[tuple[int, int, int, int]] = set()
  while 0 <= guard[0] < height and 0 <= guard[1] < width and guard + direction not in localVisited:
    localVisited.add(guard + direction)
    newSquare = (guard[0] + direction[0], guard[1] + direction[1])
    if newSquare in obstacles:
      newSquare = guard
      if direction[0] == -1:
        direction = (0, 1)
      elif direction[1] == 1:
        direction = (1, 0)
      elif direction[0] == 1:
        direction = (0, -1)
      elif direction[1] == -1:
        direction = (-1, 0)
    guard = newSquare

  if guard + direction in localVisited:
    obstructionPossibilities += 1

  obstacles.remove(possibility)

print("Part 1 solution is ", len(visited))
print("Part 2 solution is ", obstructionPossibilities)
