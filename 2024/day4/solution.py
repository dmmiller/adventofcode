
data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

with open("input.txt") as f:
  data = f.read()

grid = []
for line in data.splitlines():
  newLine = line.strip()
  grid.append(newLine)

def findXMAS(g : list[str]) -> int:

  def findString(s: str, y: int, x: int, yOffset: int, xOffset: int) -> bool:
    for i in range(len(s)):
      if 0 <= y + yOffset * i < len(g) and 0 <= x + xOffset * i < len(g[0]):
        if g[y + yOffset * i][x + xOffset * i] != s[i]:
          return False
      else:
        return False
    return True

  total = 0
  for y in range(len(g)):
    for x in range(len(g[0])):
      total += sum(findString("XMAS", y, x, yOffset, xOffset) for xOffset in range(-1,2) for yOffset in range(-1,2))

  return total

def findXMAS2(g: list[str]) -> int:
  total = 0
  for y in range(1, len(g) - 1):
    for x in range(1, len(g[0]) - 1):
      if g[y][x] == "A":
        corners = [g[y-1][x-1], g[y-1][x+1], g[y+1][x-1], g[y+1][x+1]]
        if sorted(corners) == ["M", "M", "S", "S"]:
          if g[y-1][x-1] != g[y+1][x+1]:
            total += 1
  return total


print("Part 1 solution is ", findXMAS(grid))
print("Part 2 solution is ", findXMAS2(grid))