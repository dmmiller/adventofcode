import re

data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

with open("input.txt") as f:
  data = f.read()

type Button = tuple[int, int]
type Prize = tuple[int, int]

type Machine = tuple[Button, Button, Prize]

buttonRE = re.compile(r"Button [A|B]: X\+(?P<x>\d+), Y\+(?P<y>\d+)")
prizeRE = re.compile(r"Prize: X=(?P<x>\d+), Y=(?P<y>\d+)")

rawMachines = data.split("\n\n")
machines: list[Machine] = []

for machine in rawMachines:
  a, b, prize = machine.splitlines()
  aMatch = buttonRE.match(a)
  bMatch = buttonRE.match(b)
  prizeMatch = prizeRE.match(prize)
  aButton = (int(aMatch['x']), int(aMatch['y']))
  bButton = (int(bMatch['x']), int(bMatch['y']))
  prize = (int(prizeMatch['x']), int(prizeMatch['y']))
  machines.append([aButton, bButton, prize])

def findMinToken(a: Button, b: Button, p: Prize) -> int:
  x = 0
  y = 0
  minCost = 1000
  for i in range(101):
    for j in range(101):
      if i * a[0] + j * b[0] == p[0] and i * a[1] + j * b[1] == p[1]:
        if 3 * i + j < minCost:
          minCost = 3 * i + j
  if minCost == 1000:
    return -1
  return minCost

total = 0
for machine in machines:
  cost = findMinToken(machine[0], machine[1], machine[2])
  if cost != -1:
    total += cost

print("Part 1 solution is ", total)

# total = 0
# for machine in machines:
#   cost = findMinToken(machine[0], machine[1], machine[2] + 10000000000000)
#   if cost != -1:
#     total += cost

# print("Part 2 solution is ", total)