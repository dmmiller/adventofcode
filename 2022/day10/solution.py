data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

with open("input.txt") as f:
    data = f.read()

x = 1
cycle = 1
values = {}

instructions = [line for line in data.splitlines()]

for instruction in instructions:
    values[cycle] = x
    if instruction == "noop":
        cycle += 1
    else:
        match instruction.split():
            case ["addx", value]:
                values[cycle + 1] = x
                cycle += 2
                x += int(value)
            case _:
                assert "Unknown instruction"
values[cycle] = x


def computeSignalStrength(values):
    return sum(cycle * values[cycle] for cycle in [20, 60, 100, 140, 180, 220])


print(
    f"Part 1 : The sum of the signal strength is {computeSignalStrength(values)}")


def buildPixels(values):
    pixels = []
    for row in range(6):
        for column in range(40):
            cycle = row * 40 + column + 1
            value = values[cycle]
            pixels.append("#" if column - 2 < value < column + 2 else " ")
    return pixels


pixels = buildPixels(values)


def displayPixels(pixels):
    for i in range(6):
        print("".join(pixels[40 * i: 40 * i + 40]))


print("Part 2 : ASCII Letters")
displayPixels(pixels)
