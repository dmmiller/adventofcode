from enum import Enum

data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

# with open("input.txt") as f:
#   data = f.read()

type Point = tuple[int, int]

moveMap : dict[str, Point] = {
  "<" : (-1, 0),
  "^" : (0, -1),
  ">" : (1, 0),
  "v" : (0, 1)
}

maze, moves = data.split("\n\n")
maze = maze.splitlines()
moves = moves.replace("\n", "")

def buildMaze(maze: list[str]) -> tuple[set[Point], set[Point], Point]:
  walls : set[Point] = set()
  boxes : set[Point] = set()
  robot : Point = (0,0)
  height = len(maze)
  width = len(maze[0])

  for y in range(height):
    for x in range(width):
      cell = maze[y][x]
      if cell == "#":
        walls.add((x, y))
      elif cell == "O":
        boxes.add((x, y))
      elif cell == "@":
        robot = (x, y)

  return (walls, boxes, robot)

def sumCoordinates(boxes: set[Point]) -> int:
  total = 0
  for box in boxes:
    total += 100 * box[1] + box[0]
  return total

def moveBoxes(walls: set[Point], boxes: set[Point], robot: Point) -> set[Point]:
  for move in moves:
    offset = moveMap[move]
    newPosition = (robot[0] + offset[0], robot[1] + offset[1])
    if newPosition in walls:
      pass
    elif newPosition in boxes:
      potentialEmptyPosition = (newPosition[0] + offset[0], newPosition[1] + offset[1])
      while potentialEmptyPosition in boxes:
        potentialEmptyPosition = (potentialEmptyPosition[0] + offset[0], potentialEmptyPosition[1] + offset[1])
      if potentialEmptyPosition not in walls:
        boxes.remove(newPosition)
        boxes.add(potentialEmptyPosition)
        robot = newPosition
    else:
      robot = newPosition
  return boxes

walls, boxes, robot = buildMaze(maze)
boxes = moveBoxes(walls, boxes, robot)

print("Part 1 solution is ", sumCoordinates(boxes))

class Side(Enum):
  LEFT = 1
  RIGHT = 2

def buildMaze2(maze: list[str]) -> tuple[set[Point], dict[Point, Side], Point]:
  walls : set[Point] = set()
  boxes : dict[Point, Side] = {}
  robot : Point = (0,0)
  height = len(maze)
  width = len(maze[0])

  for y in range(height):
    for x in range(width):
      cell = maze[y][x]
      if cell == "#":
        walls.add((2 * x, y))
        walls.add((2 * x + 1, y))
      elif cell == "O":
        boxes[(2 * x, y)] = Side.LEFT
        boxes[(2 * x + 1, y)] = Side.RIGHT
      elif cell == "@":
        robot = (2 * x, y)

  return (walls, boxes, robot)

def sumCoordinates2(boxes: dict[Point, Side]) -> int:
  total = 0
  for box, side in boxes.items():
    if side == Side.LEFT:
      total += 100 * box[1] + box[0]
  return total

def moveBoxes2(walls: set[Point], boxes: dict[Point, Side], robot: Point) -> dict[Point, Side]:
  for move in moves:
    offset = moveMap[move]
    newPosition = (robot[0] + offset[0], robot[1] + offset[1])
    if newPosition in walls:
      pass
    elif newPosition in boxes:
      if offset[0] != 0:
        # pushing a row of boxes horizontally
        boxesToAdjust = [newPosition]
        potentialEmptyPosition = (newPosition[0] + offset[0], newPosition[1] + offset[1])
        while potentialEmptyPosition in boxes:
          potentialEmptyPosition = (potentialEmptyPosition[0] + offset[0], potentialEmptyPosition[1] + offset[1])
          boxesToAdjust.append(potentialEmptyPosition)
        if potentialEmptyPosition not in walls:
          for box in reversed(boxesToAdjust):
            box[box[0]] = 1 # fix
          boxes.remove(newPosition)
          boxes.add(potentialEmptyPosition)
          robot = newPosition
      else:
        # pushing a box vertically which may push multiple
        pass
    else:
      robot = newPosition
  return boxes

walls, boxes, robot = buildMaze2(maze)
print(boxes)
# boxes = moveBoxes2(walls, boxes, robot)

print("Part 2 solution is ", sumCoordinates2(boxes))
