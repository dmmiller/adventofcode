from itertools import product

data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

with open("input.txt") as f:
  data = f.read()

rows: list[tuple[int, list[int]]] = []
for line in data.splitlines():
  target, values = line.split(":")
  rows.append((int(target), list(int(v) for v in values.split(" ") if len(v) > 0)))

def isPossiblyTrue(target: int, values: list[int], operators: str) -> bool:
  possibleOperators = product(operators, repeat=len(values) - 1)
  for operatorSet in possibleOperators:
    currentTotal = values[0]
    for i in range(1, len(values)):
      operator = operatorSet[i - 1]
      if operator == "*":
        currentTotal *= values[i]
      elif operator == "+":
        currentTotal += values[i]
      elif operator == "|":
        currentTotal = int(str(currentTotal) + str(values[i]))
    if currentTotal == target:
      return True
  return False

print("Part 1 solution is ", sum(row[0] if isPossiblyTrue(row[0], row[1], "*+") else 0 for row in rows))
print("Part 2 solution is ", sum(row[0] if isPossiblyTrue(row[0], row[1], "*+|") else 0 for row in rows))
