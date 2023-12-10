import re
from math import lcm

data = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

data = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

data = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

with open("input.txt") as f:
  data = f.read()

pathRE = re.compile(r"(?P<start>\w+) = \((?P<left>\w+), (?P<right>\w+)\)")

pathMap: dict[str] = {}

instructions, paths = data.split("\n\n")
for path in paths.strip().splitlines():
  m = pathRE.match(path.strip())
  pathMap[m["start"]] = (m["left"], m["right"])

location = "AAA"
ip = 0
steps = 0
while location != "ZZZ":
  steps += 1
  index = 0
  if instructions[ip] == "R":
    index = 1
  ip = (ip + 1) % len(instructions)
  location = pathMap[location][index]

print("Part 1 solution : ", steps)

locationSteps = []
locations = [key for key in pathMap.keys() if key.endswith("A")]
for location in locations:
  ip = 0
  steps = 0
  while not location.endswith("Z"):
    steps += 1
    index = 0
    if instructions[ip] == "R":
      index = 1
    ip = (ip + 1) % len(instructions)
    location = pathMap[location][index]
  locationSteps.append(steps)

print("Part 2 solution : ", lcm(*locationSteps))
