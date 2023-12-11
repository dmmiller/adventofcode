from collections import deque

data = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

with open("input.txt") as f:
  data = f.read()

connections: dict[str, list] = {
    "|": [("y", 1), ("y", -1)],
    "-": [("x", 1), ("x", -1)],
    "L": [("y", -1), ("x", 1)],
    "J": [("y", -1), ("x", -1)],
    "7": [("y", 1), ("x", -1)],
    "F": [("y", 1), ("x", 1)],
    ".": [],
    "S": [("x", 1), ("x", -1), ("y", 1), ("y", -1)],
}

rows = data.splitlines()
height = len(rows)
width = len(rows[0])
values = [[-2 for x in range(width)] for y in range(height)]

sX = 0
sY = 0

for y in range(height):
  for x in range(width):
    if (rows[y][x] == "S"):
      sX = x
      sY = y

values[sY][sX] = 0

queue = deque()
for direction, offset in connections["S"]:
  if direction == "x":
    queue.append((sX + offset, sY))
  else:
    queue.append((sX, sY + offset))

while len(queue) > 0:
  x, y = queue.popleft()
  value = -2
  others = []
  for direction, offset in connections[rows[y][x]]:
    xOffset = 0
    yOffset = 0
    if direction == "x":
      xOffset = offset
    else:
      yOffset = offset
    if values[y + yOffset][x + xOffset] != -2:
      value = values[y + yOffset][x + xOffset]
    else:
      others.append((x + xOffset, y + yOffset))
  if value != -2:
    values[y][x] = value + 1
    for other in others:
      queue.append(other)

print("Part 1 solution : ", max([max(row) for row in values]))


# replace S with proper pipe
replacement = "|"
if sY - 1 >= 0 and values[sY - 1][sX] == 1:
  if sX + 1 < width and values[sY][sX + 1] == 1:
    replacement = "L"
  elif sY + 1 < height and values[sY + 1][sX] == 1:
    replacement = "|"
  elif sX - 1 >= 0 and values[sY][sX - 1] == 1:
    replacement = "J"
  else:
    print("something wrong")
elif sX + 1 < width and values[sY][sX + 1] == 1:
  if sY + 1 < height and values[sY + 1][sX] == 1:
    replacement = "F"
  elif sX - 1 >= 0 and values[sY][sX - 1] == 1:
    replacement = "-"
  else:
    print("something wrong 2")
elif sY + 1 < height and values[sY + 1][sX] == 1:
  if sX - 1 >= 0 and values[sY][sX - 1] == 1:
    replacement = "7"
  else:
    print("something wrong 3")
else:
  print("something wrong 4")

rows[sY] = rows[sY].replace("S", replacement)

insideSquares = 0
for y in range(height):
  inside = False
  fromBottom = False
  for x in range(width):
    if values[y][x] == -2:
      if inside:
        insideSquares += 1
      continue
    pipe = rows[y][x]
    if pipe == "|":
      inside = not inside
    elif pipe == "L":
      fromBottom = False
    elif pipe == "F":
      fromBottom = True
    elif pipe == "J":
      if fromBottom:
        inside = not inside
    elif pipe == "7":
      if not fromBottom:
        inside = not inside
    elif pipe == "-":
      pass
    else:
      print("Unexpected S")

print("Part 2 solution : ",  insideSquares)
