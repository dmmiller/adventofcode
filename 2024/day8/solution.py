from itertools import combinations

data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

with open("input.txt") as f:
  data = f.read()

grid :list[str] = data.splitlines()

# these are stored in (y, x) order
antennaMap : dict[str, set[tuple[int, int]]] = {}

height = len(grid)
width = len(grid[0])
for y in range(height):
  for x in range(width):
    if grid[y][x] != ".":
      if grid[y][x] not in antennaMap:
        antennaMap[grid[y][x]] = set()
      antennaMap[grid[y][x]].add((y,x))


def generateAntinodes() -> set[tuple[int, int]]:
  antinodes = set()
  for antenna in antennaMap.values():
    for first, second in combinations(antenna, 2):
      antinode1 = (first[0] + first[0] - second[0], first[1] + first[1] - second[1])
      antinode2 = (second[0] + second[0] - first[0], second[1] + second[1] - first[1])
      if 0 <= antinode1[0] < height and 0 <= antinode1[1] < width:
        antinodes.add(antinode1)
      if 0 <= antinode2[0] < height and 0 <= antinode2[1] < width:
        antinodes.add(antinode2)
  return antinodes

def generateResonantAntinodes() -> set[tuple[int, int]]:
  antinodes = set()
  for antenna in antennaMap.values():
    for first, second in combinations(antenna, 2):
      antinodes.add(first)
      antinodes.add(second)
      for start, dir in [(first, (first[0] - second[0], first[1] - second[1])), (second, (second[0] - first[0], second[1] - first[1]))]:
        curNode = (start[0] + dir[0], start[1] + dir[1])
        while 0 <= curNode[0] < height and 0 <= curNode[1] < width:
          antinodes.add(curNode)
          curNode = (curNode[0] + dir[0], curNode[1] + dir[1])

  return antinodes


print("Part 1 solution is ", len(generateAntinodes()))
print("Part 2 solution is ", len(generateResonantAntinodes()))