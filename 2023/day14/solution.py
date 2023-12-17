
data = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""

with open("input.txt") as f:
  data = f.read()

boulders: set[tuple[int, int]] = set((x, y) for y, row in enumerate(
    data.splitlines()) for x, v in enumerate(row) if v == "O")
blocks: set[tuple[int, int]] = set((x, y) for y, row in enumerate(
    data.splitlines()) for x, v in enumerate(row) if v == "#")

blocksByColumn: dict[int, list[int]] = {}
blocksByRow: dict[int, list[int]] = {}
for block in blocks:
  column = block[0]
  row = block[1]
  if column not in blocksByColumn:
    blocksByColumn[column] = []
  if row not in blocksByRow:
    blocksByRow[row] = []
  blocksByColumn[column].append(block[1])
  blocksByRow[row].append(block[0])

for column in blocksByColumn.keys():
  blocksByColumn[column] = sorted(blocksByColumn[column])
for row in blocksByRow.keys():
  blocksByRow[row] = sorted(blocksByRow[row])

xBound = len(data.splitlines()[0])
yBound = len(data.splitlines())


def score(boulders: set[tuple[int, int]]) -> int:
  score = 0
  for boulder in boulders:
    score += (yBound - boulder[1])
  return score


def rollNorth(boulders: set[tuple[int, int]]) -> set[tuple[int, int]]:
  newBoulders = set()
  for boulder in sorted(boulders, key=lambda b: b[1]):
    column = boulder[0]
    row = boulder[1]
    start = 0
    if column in blocksByColumn:
      start = max(
          filter(lambda y: y < row, blocksByColumn[column]), default=0)
    for y in range(start, row + 1):
      newBoulder = (column, y)
      if newBoulder not in newBoulders and newBoulder not in blocks:
        newBoulders.add(newBoulder)
        break
  return newBoulders


def rollSouth(boulders: set[tuple[int, int]]) -> set[tuple[int, int]]:
  newBoulders = set()
  for boulder in reversed(sorted(boulders, key=lambda b: b[1])):
    column = boulder[0]
    row = boulder[1]
    start = yBound - 1
    if column in blocksByColumn:
      start = min(
          filter(lambda y: y > row, blocksByColumn[column]), default=yBound-1)
    for y in range(start, row - 1, -1):
      newBoulder = (column, y)
      if newBoulder not in newBoulders and newBoulder not in blocks:
        newBoulders.add(newBoulder)
        break
  return newBoulders


def rollWest(boulders: set[tuple[int, int]]) -> set[tuple[int, int]]:
  newBoulders = set()
  for boulder in sorted(boulders, key=lambda b: b[0]):
    column = boulder[0]
    row = boulder[1]
    start = 0
    if row in blocksByRow:
      start = max(
          filter(lambda x: x < column, blocksByRow[row]), default=0)
    for x in range(start, column + 1):
      newBoulder = (x, row)
      if newBoulder not in newBoulders and newBoulder not in blocks:
        newBoulders.add(newBoulder)
        break
  return newBoulders


def rollEast(boulders: set[tuple[int, int]]) -> set[tuple[int, int]]:
  newBoulders = set()
  for boulder in reversed(sorted(boulders, key=lambda b: b[0])):
    column = boulder[0]
    row = boulder[1]
    start = xBound - 1
    if row in blocksByRow:
      start = min(
          filter(lambda x: x > column, blocksByRow[row]), default=xBound - 1)
    for x in range(start, column - 1, -1):
      newBoulder = (x, row)
      if newBoulder not in newBoulders and newBoulder not in blocks:
        newBoulders.add(newBoulder)
        break
  return newBoulders


def cycle(boulders: set[tuple[int, int]]) -> set[tuple[int, int]]:
  boulders = rollNorth(boulders)
  boulders = rollWest(boulders)
  boulders = rollSouth(boulders)
  return rollEast(boulders)


def pretty(boulders: set[tuple[int, int]]) -> None:
  for y in range(yBound):
    for x in range(xBound):
      ch = "."
      if (x, y) in boulders:
        ch = "O"
      if (x, y) in blocks:
        ch = "#"
      print(ch, end="")
    print("")


print("Part 1 solution : ", score(rollNorth(boulders)))

# assuming a cycle of values so just find those values
# and then see which one would extrapolate to the right value
cycleDetector: dict[int, list[int]] = {}
hashToScore: dict[int, int] = {}
first = ""
# 350 is just ballpark that we will have found the cycle from trial and error
for i in range(350):
  boulders = cycle(boulders)
  s = score(boulders)
  h = hash(frozenset(boulders))
  if h not in hashToScore:
    hashToScore[h] = s
  if h not in cycleDetector:
    cycleDetector[h] = []
  cycleDetector[h].append(i + 1)

for k, v in cycleDetector.items():
  if len(v) > 2:
    diff = v[-1] - v[-2]
    mod = 1000000000 % diff
    if mod + diff in v:
      print('Part 2 solution : ', hashToScore[k])
