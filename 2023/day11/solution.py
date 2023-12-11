data = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

with open("input.txt") as f:
  data = f.read()

galaxyMap = [line for line in data.splitlines()]

originalGalaxies: list[tuple[int, int]] = []

for y in range(len(galaxyMap)):
  for x in range(len(galaxyMap[0])):
    if galaxyMap[y][x] == "#":
      originalGalaxies.append((x, y))

# check for expansion rows
expansionRows: list[int] = []
for y in range(len(galaxyMap)):
  for x in range(len(galaxyMap[0])):
    if galaxyMap[y][x] == "#":
      break
  else:
    expansionRows.append(y)

# check for expansion columns
expansionColumns: list[int] = []
for x in range(len(galaxyMap[0])):
  for y in range(len(galaxyMap)):
    if galaxyMap[y][x] == "#":
      break
  else:
    expansionColumns.append(x)


def expandGalaxies(galaxies: list[tuple[int, int]], expansionValue, expansionRows, expansionColumns):
  newGalaxies = []
  for galaxy in galaxies:
    xAdjustment = len(list(filter(lambda x: x < galaxy[0], expansionColumns)))
    yAdjustment = len(list(filter(lambda y: y < galaxy[1], expansionRows)))
    newGalaxies.append((galaxy[0] + xAdjustment * (expansionValue - 1),
                        galaxy[1] + yAdjustment * (expansionValue - 1)))
  return newGalaxies


def computeDistance(galaxies: list[tuple[int, int]]) -> int:
  distance = 0
  for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
      distance += (abs(galaxies[i][0] - galaxies[j][0]) +
                   abs(galaxies[i][1] - galaxies[j][1]))
  return distance


part1Galaxies = expandGalaxies(
    originalGalaxies, 2, expansionRows, expansionColumns)
part2Galaxies = expandGalaxies(
    originalGalaxies, 1000000, expansionRows, expansionColumns)

print("Part 1 solution : ", computeDistance(part1Galaxies))
print("Part 2 solution : ", computeDistance(part2Galaxies))
