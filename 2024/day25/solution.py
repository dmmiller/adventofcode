data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

with open("input.txt") as f:
  data = f.read()


def buildLocksAndKeys(items: list[str]) -> tuple[list[list[int]], list[list[int]]]:
  keys: list[list[int]] = []
  locks: list[list[int]] = []

  width = 5
  height = 7
  for item in items:
    rows = item.splitlines()
    if rows[0][0] == '#':
      # lock
      lock = []
      for x in range(width):
        for y in range(height):
          if rows[y][x] == '.':
            lock.append(y - 1)
            break
      locks.append(lock)
    else:
      # key
      key = []
      for x in range(width):
        for y in range(height):
          if rows[height - y - 1][x] == '.':
            key.append(y - 1)
            break
      keys.append(key)

  return (locks, keys)

def overlapCount(locks: list[list[int]], keys: list[list[int]]) -> int:
  count = 0
  for lock in locks:
    for key in keys:
      for x in range(len(lock)):
        if lock[x] + key[x] > 5:
          break
      else:
        count += 1
  return count

locks, keys = buildLocksAndKeys(data.split("\n\n"))
print("Part 1 solution is ", overlapCount(locks, keys))
