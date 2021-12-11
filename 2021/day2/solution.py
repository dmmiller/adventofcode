import re

with open("input.txt") as f:
    instructions = [x.strip() for x in f.readlines()]

re_inst = re.compile(r"(?P<direction>\w+) (?P<value>\d+)")
position = 0
depth = 0
for inst in instructions:
    match = re_inst.match(inst)
    delta = int(match['value'])
    if match['direction'] == "forward":
        position += delta
    elif match['direction'] == "down":
        depth += delta
    elif match['direction'] == "up":
        depth -= delta

print(f"Part 1")
print(f"Final position {position}")
print(f"Final depth {depth}")
print(f"Product {position * depth}")

position = 0
depth = 0
aim = 0
for inst in instructions:
    match = re_inst.match(inst)
    delta = int(match['value'])
    if match['direction'] == "forward":
        position += delta
        depth += (aim * delta)
    elif match['direction'] == "down":
        aim += delta
    elif match['direction'] == "up":
        aim -= delta

print(f"Part 2")
print(f"Final position {position}")
print(f"Final depth {depth}")
print(f"Product {position * depth}")
