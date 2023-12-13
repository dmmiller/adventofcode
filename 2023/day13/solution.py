
data = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""

with open("input.txt") as f:
  data = f.read()


class Valley:
  rows: list[int]
  columns: list[int]

  def __init__(self, rows) -> None:
    self.rows = [int(row.replace(".", "0").replace("#", "1"), 2)
                 for row in rows]
    self.columns = [int("".join([row[i] for row in rows]).replace(".", "0").replace("#", "1"), 2)
                    for i in range(len(rows[0]))]

  def summarize(self) -> int:

    def computeMirror(rows: list[int], multiplier: int) -> int:
      rowCount = len(rows)
      for i in range(1, rowCount):
        if rows[i] == rows[i - 1]:
          reflectionCount = min(i, rowCount - i)
          for j in range(reflectionCount):
            if rows[i - j - 1] != rows[i + j]:
              break
          else:
            return i * multiplier
      return -1

    if (value := computeMirror(self.rows, 100)) > 0:
      return value
    return computeMirror(self.columns, 1)

  def smudgarize(self) -> int:
    def differByOne(v1: int, v2: int) -> bool:
      v = v1 ^ v2
      return v.bit_count() == 1

    def computeSmudgeMirror(rows: list[int], multiplier: int) -> int:
      rowCount = len(rows)
      for i in range(rowCount):
        for j in range(i + 1, rowCount, 2):
          if differByOne(rows[i], rows[j]):
            mid = int((i + j + 1) / 2)
            reflectionCount = min(mid, rowCount - mid)
            for k in range(reflectionCount):
              if mid - k - 1 == i and mid + k == j:
                continue
              if rows[mid - k - 1] != rows[mid + k]:
                break
            else:
              return mid * multiplier
      return -1

    if (value := computeSmudgeMirror(self.rows, 100)) > 0:
      return value
    return computeSmudgeMirror(self.columns, 1)


valleys: list[Valley] = [Valley(v.splitlines()) for v in data.split("\n\n")]

print("Part 1 solution : ", sum(valley.summarize() for valley in valleys))
print("Part 1 solution : ", sum(valley.smudgarize() for valley in valleys))
