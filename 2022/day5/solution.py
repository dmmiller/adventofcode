from collections import deque
import re

data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

with open("input.txt") as f:
    data = f.read()

crate_info, instructions = data.split("\n\n")
initial_crates = crate_info.splitlines()
initial_stacks = [deque() for i in range(0, len(initial_crates[0]) + 1, 4)]
for i in range(len(initial_crates) - 1):
    row = initial_crates[i]
    for j in range(0, len(row), 4):
        bracket = row[j:j+4].find("[")
        if bracket != -1:
            value = row[j:j+4][bracket + 1]
            initial_stacks[int(j / 4)].append(value)


instruction_matcher = re.compile(
    r"move (?P<count>\d+) from (?P<src>\d+) to (?P<dest>\d+)")

part1_stacks = [deque(s) for s in initial_stacks]
part2_stacks = [deque(s) for s in initial_stacks]

for instruction in instructions.splitlines():
    value = instruction_matcher.match(instruction)
    count = int(value['count'])
    src_index = int(value['src']) - 1
    dest_index = int(value['dest']) - 1
    for i in range(count):
        part1_stacks[dest_index].appendleft(
            part1_stacks[src_index].popleft())
    temp_stack = deque()
    for i in range(count):
        temp_stack.appendleft(part2_stacks[src_index].popleft())
    part2_stacks[dest_index].extendleft(temp_stack)

print(f"Part 1: Top of stacks are {''.join((s[0] for s in part1_stacks))}")
print(f"Part 2: Top of stacks are {''.join((s[0] for s in part2_stacks))}")
