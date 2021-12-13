import re

example = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

instruction_re = re.compile(r"fold along (?P<axis>[xy])=(?P<value>\d+)")

with open("input.txt") as f:
    coordinates, instructions = example.split("\n\n")
    coordinates, instructions = f.read().split("\n\n")
    dots = set()
    for coord in coordinates.strip().split("\n"):
        dots.add(tuple(int(value) for value in coord.strip().split(",")))
    folds = []
    for instruction in instructions.strip().split("\n"):
        result = instruction_re.match(instruction.strip())
        folds.append((result['axis'], int(result['value'])))

def fold(coordinates, axis, value):
    new_coordinates = set()
    for coordinate in coordinates:
        if axis == 'x' and coordinate[0] > value:
            new_coordinates.add((value - (coordinate[0] - value), coordinate[1]))
        elif axis == 'y' and coordinate[1] > value:
            new_coordinates.add((coordinate[0], value - (coordinate[1] - value)))
        else:
            new_coordinates.add(coordinate)
    return new_coordinates

fold_once = fold(dots, folds[0][0], folds[0][1])
print(f"Part 1 has {len(fold_once)} dots visible")

for instruction in folds:
    dots = fold(dots, instruction[0], instruction[1])

def print_dots(dots):
    max_x = max(dot[0] for dot in dots) + 1
    max_y = max(dot[1] for dot in dots) + 1
    rows = [[' ' for x in range(max_x)] for y in range(max_y)]
    for dot in dots:
        rows[dot[1]][dot[0]] = "#"
    print("Part 2 code is ")
    for row in rows:
        print("".join(row))

print_dots(dots)