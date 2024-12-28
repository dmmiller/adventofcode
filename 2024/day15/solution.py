from enum import Enum
from itertools import chain

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

with open("input.txt") as f:
  data = f.read()

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

def printBoard(walls: set[Point], boxes: dict[Point, Side], robot: Point, move: str):
  height = max(point[1] for point in walls) + 1
  width = max(point[0] for point in walls) + 1
  for y in range(height):
    for x in range(width):
      point: Point = (x, y)
      if point in walls:
        print("#", end="")
      elif point in boxes:
        if boxes[point] == Side.LEFT:
          print("[", end="")
        else:
          print("]", end="")
      elif point == robot:
        print(move, end="")
      else:
        print(".", end="")
    print("")
  print("")

def moveBoxes2(walls: set[Point], boxes: dict[Point, Side], robot: Point) -> dict[Point, Side]:
  for move in moves:
    # printBoard(walls, boxes, robot, move)
    offset = moveMap[move]
    newPosition = (robot[0] + offset[0], robot[1] + offset[1])
    if newPosition in walls:
      pass
    elif newPosition in boxes:
      if offset[0] != 0:
        # pushing a row of boxes horizontally
        boxesToAdjust = [newPosition]
        potentialEmptyPosition = (newPosition[0] + offset[0], newPosition[1])
        while potentialEmptyPosition in boxes:
          boxesToAdjust.append(potentialEmptyPosition)
          potentialEmptyPosition = (potentialEmptyPosition[0] + offset[0], potentialEmptyPosition[1])
        if potentialEmptyPosition not in walls:
          for box in reversed(boxesToAdjust):
            side = boxes[box]
            del boxes[box]
            boxes[(box[0] + offset[0], box[1])] = side
          robot = newPosition
      else:
        # pushing a box vertically which may push multiple
        left = newPosition[0]
        right = newPosition[0]
        if boxes[newPosition] == Side.LEFT:
          right = right + 1
        else:
          left = left - 1
        boxesToAdjust: list[Point] = []
        fringe: list[Point] = [(left, newPosition[1]), (right, newPosition[1])]
        while True:
          potentialEmptyPositions = [(point[0], point[1] + offset[1]) for point in fringe]
          if any(point in walls for point in potentialEmptyPositions):
            # fringe hits wall so can not move
           break
          elif all(point not in boxes for point in potentialEmptyPositions):
            # empty space at fringe so move robot
            for box in reversed(list(chain(boxesToAdjust, fringe))):
              side = boxes[box]
              del boxes[box]
              boxes[(box[0], box[1] + offset[1])] = side
            robot = newPosition
            break
          else:
            # hit at least one box
            boxesToAdjust.extend(fringe)
            fringe = []
            for potentialEmptyPosition in potentialEmptyPositions:
              if potentialEmptyPosition in boxes:
                side = boxes[potentialEmptyPosition]
                if side == Side.LEFT:
                  left = potentialEmptyPosition
                  right = (potentialEmptyPosition[0] + 1, potentialEmptyPosition[1])
                else:
                  left = (potentialEmptyPosition[0] - 1, potentialEmptyPosition[1])
                  right = potentialEmptyPosition
                if left not in fringe:
                  fringe.append(left)
                if right not in fringe:
                  fringe.append(right)
    else:
      robot = newPosition
  return boxes

walls, boxes, robot = buildMaze2(maze)
boxes = moveBoxes2(walls, boxes, robot)

print("Part 2 solution is ", sumCoordinates2(boxes))
