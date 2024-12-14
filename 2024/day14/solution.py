import re

data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
height = 7
width = 11

with open("input.txt") as f:
  data = f.read()
height = 103
width = 101


type Position = tuple[int, int]
type Velocity = tuple[int, int]
type Robot = tuple[Position, Velocity]

robots : list[Robot] = []
regex = re.compile(r"p=(?P<px>-?\d+),(?P<py>-?\d+) v=(?P<vx>-?\d+),(?P<vy>-?\d+)")

for line in data.splitlines():
  m = regex.match(line)
  robots.append(((int(m['px']), int(m['py'])), (int(m['vx']), int(m['vy']))))

def moveRobot(robot: Robot, moves: int) -> Robot:
  x, y = robot[0]
  deltax, deltay = robot[1]
  x += moves * deltax
  y += moves * deltay
  return ((x % width, y % height), (deltax, deltay))

def computeSafetyFactor(robots: list[Robot]) -> int:
  locations : dict[Position, int] = {}
  for robot in robots:
    if robot[0] not in locations:
      locations[robot[0]] = 0
    locations[robot[0]] += 1

  midx = width // 2
  midy = height // 2

  score = 1
  for quadrant in [(0, midx, 0, midy), (midx + 1, width, 0, midy), (0, midx, midy + 1, height), (midx + 1, width, midy + 1, height)]:
    quadrantCount = 0
    for x in range(quadrant[0], quadrant[1]):
      for y in range(quadrant[2], quadrant[3]):
        if (x, y) in locations:
          quadrantCount += locations[(x, y)]
    score *= quadrantCount

  return score

translatedRobots = [moveRobot(robot, 100) for robot in robots]

print("Part 1 solution is ", computeSafetyFactor(translatedRobots))