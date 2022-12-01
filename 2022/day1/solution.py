data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""

with open("input.txt") as f:
    data = f.read()

elves = [[int(v) for v in line.split("\n")] for line in data.split("\n\n")]
elves.sort(reverse=True, key=lambda elf: sum(elf))

print(f"Part 1 is {sum(elves[0])}")
print(f"Part 2 is {sum(sum(elves[i]) for i in range(3))}")