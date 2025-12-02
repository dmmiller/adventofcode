data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

with open("input.txt") as f:
  data = f.read()

zeroCounter = 0
zeroTouches = 0
pointer = 50
for line in data.splitlines():
    line = line.strip()
    amount = int(line[1:])
    oldPointer = pointer
    increment = 1
    if line[0] == "L":
        amount = 0 - amount
        increment = -1
    for i in range(0, amount, increment):
        pointer = pointer + increment
        if pointer % 100 == 0:
            zeroTouches += 1
    if pointer % 100 == 0:
        zeroCounter += 1

print("Part 1 solution is ", zeroCounter)
print("Part 2 solution is ", zeroTouches)
