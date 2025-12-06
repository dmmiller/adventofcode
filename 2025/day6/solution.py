from math import prod

data = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

with open("input.txt") as f:
  data = f.read()

lines = [[item for value in line.strip().split(" ") if (item := value.strip()) and len(item)] for line in data.splitlines()]

equations = []
for i in range(len(lines[0])):
  equation = []
  if lines[-1][i] == '*':
    equation.append(prod)
  else:
    equation.append(sum)
  for j in range(len(lines) - 1):
    equation.append(int(lines[j][i]))
  equations.append(equation)

part1Solution = sum(equation[0](equation[1:]) for equation in equations)
print("Part 1 solution is ", part1Solution)

lines = data.splitlines()
part2Solution = 0
i = len(lines[0]) - 1
while i >= 0:
  def computeColumnValue():
    value = 0
    for r in range(len(lines) - 1):
      if lines[r][i] != ' ':
        value = 10 * value + int(lines[r][i])
    return value
  numbers = []
  operation = None
  while True and i >= 0:
    number = computeColumnValue()
    if number == 0:
      break
    numbers.append(number)
    if lines[-1][i] == '*':
      operation = prod
    elif lines[-1][i] == '+':
      operation = sum
    i -= 1
  part2Solution += operation(numbers)
  i -= 1

print("Part 2 solution is ", part2Solution)