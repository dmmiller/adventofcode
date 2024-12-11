from functools import cache

data = """125 17"""

with open("input.txt") as f:
  data = f.read()

initial = {}
for i in data.split(" "):
  v = int(i)
  if v not in initial:
    initial[v] = 0
  initial[v] += 1

@cache
def transformStone(value: int) -> list[int]:
  if value == 0:
    return [1]
  if len(str(value)) % 2 == 0:
    s = str(value)
    return [int(s[0 : len(s) // 2]), int(s[len(s) // 2 : ])]
  return [value * 2024]

def blink(input: dict[int, int]) -> dict[int, int]:
  output = {}
  for k, v in input.items():
    newItems = transformStone(k)
    for ni in newItems:
      if ni not in output:
        output[ni] = 0
      output[ni] += v
  return output

for i in range(25):
  initial = blink(initial)
print("Part 1 solution is ", sum(v for v in initial.values()))

for i in range(50):
  initial = blink(initial)
print("Part 2 solution is ", sum(v for v in initial.values()))