from functools import cache

data = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

with open("input.txt") as f:
  data = f.read()


def countOptions(line: str) -> int:
  pattern, values = line.split(" ")
  values = list(map(lambda x: int(x), values.split(",")))

  @cache
  def recurse(characterIndex: int, valueIndex: int, currentCount: int) -> int:
    def handlePound():
      if valueIndex < len(values) and currentCount < values[valueIndex]:
        return recurse(characterIndex + 1, valueIndex, currentCount + 1)
      return 0

    def handleDot():
      if currentCount > 0:
        if valueIndex < len(values) and currentCount == values[valueIndex]:
          return recurse(characterIndex + 1, valueIndex + 1, 0)
        return 0
      else:
        return recurse(characterIndex + 1, valueIndex, 0)

    if characterIndex == len(pattern):
      if currentCount > 0:
        if valueIndex < len(values) and currentCount == values[valueIndex]:
          valueIndex += 1
      if valueIndex != len(values):
        return 0
      return 1
    c = pattern[characterIndex]
    if c == "#":
      return handlePound()
    elif c == ".":
      return handleDot()
    else:
      # handle if the ? were a # or a . and add up possiblities
      return handlePound() + handleDot()

  return recurse(0, 0, 0)


print("Part 1 solution : ", sum(map(lambda l: countOptions(l), data.splitlines())))
part2 = 0
for line in data.splitlines():
  left, right = line.split(" ")
  part2 += countOptions("?".join([left for i in range(5)])
                        + " "
                        + ",".join([right for i in range(5)])
                        )
print("Part 2 solution : ", part2)
