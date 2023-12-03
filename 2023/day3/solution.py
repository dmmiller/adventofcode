
data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

with open("input.txt") as f:
  data = f.read()


grid: list[list[str]] = [row for row in data.split("\n")]

width: int = len(grid[0])
height: int = len(grid)

part1Total = 0
for y in range(height):
  value = 0
  adjacent = False
  for x in range(width):
    if grid[y][x].isnumeric():
      value = 10 * value + int(grid[y][x])
      for xOffset in range(-1, 2):
        for yOffset in range(-1, 2):
          if 0 <= x + xOffset < width and 0 <= y + yOffset < height:
            if not grid[y + yOffset][x + xOffset].isnumeric() and grid[y + yOffset][x + xOffset] != '.':
              adjacent = True
    else:
      if adjacent:
        part1Total += value
      value = 0
      adjacent = False
  else:
    if adjacent:
      part1Total += value
print("Part 1 solution : ", part1Total)

gears = {}
for y in range(height):
  rowGears = set()
  for x in range(width):
    if grid[y][x].isnumeric():
      value = 10 * value + int(grid[y][x])
      for xOffset in range(-1, 2):
        for yOffset in range(-1, 2):
          if 0 <= x + xOffset < width and 0 <= y + yOffset < height:
            if not grid[y + yOffset][x + xOffset].isnumeric() and grid[y + yOffset][x + xOffset] == '*':
              rowGears.add((y + yOffset, x + xOffset))
    else:
      if len(rowGears) > 0:
        for gear in rowGears:
          if gear not in gears:
            gears[gear] = []
          gears[gear].append(value)
      value = 0
      rowGears = set()
  else:
    if len(rowGears) > 0:
      for gear in rowGears:
        if gear not in gears:
          gears[gear] = []
        gears[gear].append(value)


part2Total = 0
for gear in gears:
  if len(gears[gear]) == 2:
    part2Total += (gears[gear][0] * gears[gear][1])

print("Part 2 solution : ", part2Total)
