from functools import cache

data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

with open("input.txt") as f:
  data = f.read()

patterns, designs = data.split("\n\n")

patterns = set(patterns.split(', '))
maxLenPattern = len(max(patterns, key=len))
designs = designs.splitlines()

@cache
def isValid(design: str) -> bool:
  if design in patterns or len(design) == 0:
    return True
  for i in range(1, maxLenPattern + 1):
    if design[:i] in patterns:
      if isValid(design[i:]):
        return True
  return False

@cache
def validWays(design: str) -> int:
  if len(design) == 0:
    return 0
  total = 1 if design in patterns else 0
  for i in range(1, maxLenPattern + 1):
    if design[:i] in patterns:
      total += validWays(design[i:])
  return total

print("Part 1 solution is ", sum(1 if isValid(design) else 0 for design in designs))
print("Part 2 solution is ", sum(validWays(design) for design in designs))