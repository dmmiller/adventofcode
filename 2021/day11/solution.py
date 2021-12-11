example = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

with open("input.txt") as f:
    octopi = [[int(value) for value in line.strip()] for line in f.readlines()]
#    octopi = [[int(value) for value in line.strip()] for line in example.split("\n")]

print(octopi)
flash_count = 0
step = 0
while True:
    step += 1
    # increment all by 1
    octopi = [[value + 1 for value in row] for row in octopi]
    changed = True
    flashed = set()
    while changed:
        changed = False
        for y in range(10):
            for x in range(10):
                if octopi[y][x] > 9  and (y,x) not in flashed:
                    flash_count += 1
                    changed = True
                    flashed.add((y,x))
                    for ymod in [-1, 0, 1]:
                        for xmod in [-1, 0, 1]:
                            if 0 <= y + ymod < 10 and 0 <= x + xmod < 10:
                                octopi[y + ymod][x + xmod] += 1
    for pt in flashed:
        octopi[pt[0]][pt[1]] = 0
    if sum(value for row in octopi for value in row) == 0:
        print(f"Part 2 all flash at Step {step}")
        break
    if step == 100:
        print(f"Part 1 : total flash count {flash_count}")
