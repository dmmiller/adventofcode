from functools import cache

data = """029A
980A
179A
456A
379A"""

with open("input.txt") as f:
  data = f.read()

# data = """340A"""

type Point = tuple[int, int]
type MoveMap = dict[tuple[str, str], list[str]]


numericPad = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], [None, '0', 'A']]
directionPad = [[None, '^', 'A'], ['<', 'v', '>']]

def genMoveMap(pad: list[list[str|None]]) -> MoveMap:

  def pathHitsHole(point: Point, path: str, hole: Point) -> bool:
    for d in path:
      match d:
        case '>':
          point = (point[0] + 1, point[1])
        case '<':
          point = (point[0] - 1, point[1])
        case '^':
          point = (point[0], point[1] - 1)
        case 'v':
          point = (point[0], point[1] + 1)
      if point == hole:
        return True
    return False

  height = len(pad)
  width = len(pad[0])
  keyMap: dict[str, Point] = {}
  hole: Point = (0, 0)
  minPathMap: MoveMap = {}
  for y in range(height):
    for x in range(width):
      if pad[y][x] != None:
        keyMap[pad[y][x]] = (x, y)
      else:
        hole = (x, y)

  for start in keyMap.keys():
    for end in keyMap.keys():
      path = ''
      startPoint = keyMap[start]
      endPoint = keyMap[end]
      while startPoint != endPoint:
        # try to move in x direction
        if startPoint[0] != endPoint[0]:
          if startPoint[0] < endPoint[0] and (startPoint[0] + 1, startPoint[1]) != hole:
            startPoint = (startPoint[0] + 1, startPoint[1])
            path += '>'
          elif startPoint[0] > endPoint[0] and (startPoint[0] - 1, startPoint[1]) != hole:
            startPoint = (startPoint[0] - 1, startPoint[1])
            path += '<'
        # try to move in y direction
        if startPoint[1] != endPoint[1]:
          if startPoint[1] < endPoint[1] and (startPoint[0], startPoint[1] + 1) != hole:
            startPoint = (startPoint[0], startPoint[1] + 1)
            path += 'v'
          if startPoint[1] > endPoint[1] and (startPoint[0], startPoint[1] - 1) != hole:
            startPoint = (startPoint[0], startPoint[1] - 1)
            path += '^'

      # sort path to minimize zig zags which cost keystrokes
      # check path sorted and reverse sorted to make sure you don't hit hole
      minPathMap[(start, end)] = []
      path = ''.join(sorted(path))
      reversePath = ''.join(reversed(path))
      if path == reversePath:
        minPathMap[(start, end)].append(path)
      else:
        if not pathHitsHole(keyMap[start], path, hole):
          minPathMap[(start, end)].append(path)
        if not pathHitsHole(keyMap[start], reversePath, hole):
          minPathMap[(start, end)].append(reversePath)

  return minPathMap

numericMoveMap = genMoveMap(numericPad)
directionMoveMap = genMoveMap(directionPad)

def cost(path: str, pad: MoveMap) -> int:
  movement = 0
  previous = 'A'
  for c in path:
    movement += len(pad[(previous, c)])
    previous = c
  return movement

@cache
def getSequences2(sequence: str, pad: MoveMap):
  pass

def getSequences(sequence: str, moveMap: MoveMap) -> set[str]:
  print(f"generating paths for sequence of length {len(sequence)}")
  previous = 'A'
  paths = set()
  paths.add('')
  for c in sequence:
    moves = moveMap[(previous, c)]
    for path in paths.copy():
      paths.remove(path)
      for move in moves:
        paths.add(path + move + 'A')
    previous = c
  print(f"Sequence of length {len(sequence)} generates {len(paths)} options")
  return paths


def findSuperPath(target: str, chain: int, numberPad: MoveMap, dPad: MoveMap) -> str:

  def minCostTargets(targets: set[str], pad: MoveMap) -> set[str]:
    costMap: dict[int, set[str]] = {}
    lenMap: dict[int, set[str]] = {}
    for target in targets:
      targetCost = cost(target, pad)
      if targetCost not in costMap:
        costMap[targetCost] = set()
      costMap[targetCost].add(target)
      if len(target) not in lenMap:
        lenMap[len(target)] = set()
      lenMap[len(target)].add(target)
    minSet = costMap[min(k for k in costMap.keys())].intersection(lenMap[min(k for k in lenMap.keys())])
    return set([minSet.pop()])

  def doThings(remaining: int, targets: set[str], pad: MoveMap) -> set[str]:
    print(f"Considering {len(targets)} size set at {remaining}")
    if remaining == 0:
      return targets
    newTargets = set()
    for target in targets:
      newTargets |= getSequences(target, pad)
      print('new targets is currently size : ', len(newTargets))
    newTargets = minCostTargets(newTargets, pad)
    return doThings(remaining - 1, newTargets, pad)

  final = getSequences(target, numberPad)
  woo = doThings(chain, final, dPad)
  pathLengths: dict[int, str] = {}
  pathCosts: dict[int, str] = {}
  for w in woo:
    pathLengths[len(w)] = w
    pathCosts[cost(w, dPad)] = w
  print(len(woo))
  print(pathLengths)
  print(pathCosts)
  return pathLengths[min(k for k in pathLengths.keys())]


  pathLengths: dict[int, str] = {}
  pathCosts: dict[int, str] = {}
  finalPaths = set()
  for finalRobotPath in getSequences(target, numberPad):
    for penultimateRobotPath in getSequences(finalRobotPath, dPad):
      for initialRobotPath in getSequences(penultimateRobotPath, dPad):
        path = initialRobotPath
        finalPaths.add(path)
        pathLengths[len(path)] = path
        pathCosts[cost(path, dPad)] = path
  print('considered paths', len(finalPaths))
  print('lengths', pathLengths)
  print('costs', pathCosts)
  return pathLengths[min(k for k in pathLengths.keys())]

def complexity(code: str, chain: int, numberPad: MoveMap, dPad: MoveMap) -> int:
  path = findSuperPath(code, chain, numberPad, dPad)
  number = int(code[:-1])
  return number * len(path)

print("Part 1 solution is", sum(complexity(code, 2, numericMoveMap, directionMoveMap) for code in data.splitlines()))
print("Part 2 solution is", sum(complexity(code, 25, numericMoveMap, directionMoveMap) for code in data.splitlines()))