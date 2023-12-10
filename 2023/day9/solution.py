data = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

with open("input.txt") as f:
  data = f.read()

rows = [list(map(lambda x: int(x.strip()), line.split(" ")))
        for line in data.splitlines()]


def genNextValue(row: list[int]) -> int:
  if all(map(lambda x: x == 0, row)):
    return 0
  return row[-1] + genNextValue([row[count + 1] - value for count, value in enumerate(row) if count + 1 < len(row)])


print("Part 1 solution : ", sum(genNextValue(row) for row in rows))
print("Part 2 solution : ", sum(genNextValue(list(reversed(row)))
      for row in rows))
