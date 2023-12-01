data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

with open("input.txt") as f:
  data = f.read()


def parseLine1(s: str) -> int:
  first = -1
  last = -1
  for i in range(len(s)):
    if s[i].isnumeric():
      num = int(s[i])
      if first == -1:
        first = num
      last = num
  return 10 * first + last


numberMap = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def parseLine2(s: str) -> int:
  first = -1
  last = -1
  for i in range(len(s)):
    num = -1
    if s[i].isnumeric():
      num = int(s[i])
    elif (
        s[i: i + 3] in numberMap
        or s[i: i + 4] in numberMap
        or s[i: i + 5] in numberMap
    ):
      for e in range(3, 6):
        if s[i: i + e] in numberMap:
          num = numberMap[s[i: i + e]]
          break

    if num != -1:
      if first == -1:
        first = num
      last = num

  return 10 * first + last


part1Total = 0
part2Total = 0
for line in data.splitlines():
  part1Total += parseLine1(line)
  part2Total += parseLine2(line)

print("Part 1 solution is ", part1Total)
print("Part 2 solution is ", part2Total)
