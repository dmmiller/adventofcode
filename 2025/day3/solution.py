data = """987654321111111
811111111111119
234234234234278
818181911112111"""

with open("input.txt") as f:
  data = f.read()

def joltage(s: str) -> int:
  tens = 0
  tensIndex = 0
  for i in range(len(s) - 1):
    if int(s[i]) > tens:
      tens = int(s[i])
      tensIndex = i
  ones  = 0
  for i in range(tensIndex + 1, len(s)):
    if int(s[i]) > ones:
      ones = int(s[i])
  return tens * 10 + ones

def joltage2(s: str, size: int) -> int:
  def inner(startingIndex: int, sizeRemaining: int) -> int:
    maxIndex = startingIndex
    for i in range(startingIndex, len(s) - (sizeRemaining - 1)):
      if int(s[i]) > int(s[maxIndex]):
        maxIndex = i
    return maxIndex

  value = 0
  index = 0
  while size > 0:
    highestIndex = inner(index, size)
    value = value * 10 + int(s[highestIndex])
    index = highestIndex + 1
    size = size - 1

  return value


part1JoltageSum = sum(joltage(line) for line in data.splitlines())
print("Part 1 solution is ", part1JoltageSum)

part2JoltageSum = sum(joltage2(line, 12) for line in data.splitlines())
print("Part 2 solution is ", part2JoltageSum)

