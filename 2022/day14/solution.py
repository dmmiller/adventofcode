data = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

with open("input.txt") as f:
    data = f.read()


def buildAbyss(rocks: list[str]):
    abyss = {}
    for rock in rocks:
        previous_x = -1
        previous_y = -1
        for path in rock.split(" -> "):
            new_x, new_y = map(int, path.split(","))
            abyss[(new_x, new_y)] = '#'
            if previous_x != -1 and previous_y != -1:
                assert previous_x == new_x or previous_y == new_y
                for x in range(min(new_x, previous_x), max(new_x, previous_x) + 1):
                    for y in range(min(new_y, previous_y), max(new_y, previous_y) + 1):
                        abyss[(x, y)] = '#'
            previous_x = new_x
            previous_y = new_y
    return abyss


def countGrainsUntilFalling(abyss: dict[tuple, str]) -> int:
    origin = (500, 0)
    max_depth = 0
    for k_x, k_y in abyss.keys():
        if k_y > max_depth:
            max_depth = k_y
    totalSand = 0
    settles = True
    while settles:
        stillMoving = True
        sand = origin
        while stillMoving:
            if sand[1] > max_depth:
                settles = False
                break
            target = (sand[0], sand[1] + 1)
            if target not in abyss:
                sand = target
            else:
                target = (sand[0] - 1, sand[1] + 1)
                if target not in abyss:
                    sand = target
                else:
                    target = (sand[0] + 1, sand[1] + 1)
                    if target not in abyss:
                        sand = target
                    else:
                        stillMoving = False
                        totalSand += 1
                        abyss[sand] = 'o'

    return totalSand


def countGrainsUntilFull(abyss: dict[tuple, str]) -> int:
    origin = (500, 0)
    max_depth = 0
    for k_x, k_y in abyss.keys():
        if k_y > max_depth:
            max_depth = k_y
    totalSand = 0
    while origin not in abyss:
        stillMoving = True
        sand = origin
        while stillMoving:
            if sand[1] == max_depth + 1:
                stillMoving = False
                totalSand += 1
                abyss[sand] = 'o'
                break
            target = (sand[0], sand[1] + 1)
            if target not in abyss:
                sand = target
            else:
                target = (sand[0] - 1, sand[1] + 1)
                if target not in abyss:
                    sand = target
                else:
                    target = (sand[0] + 1, sand[1] + 1)
                    if target not in abyss:
                        sand = target
                    else:
                        stillMoving = False
                        totalSand += 1
                        abyss[sand] = 'o'

    return totalSand


abyss = buildAbyss([rocks for rocks in data.splitlines()])
print(f"Part 1 : Sand fills after {countGrainsUntilFalling(abyss)} grains")

abyss = buildAbyss([rocks for rocks in data.splitlines()])
print(f"Part 2 : Total sand to fill chamber is {countGrainsUntilFull(abyss)}")
