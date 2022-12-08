data = """30373
25512
65332
33549
35390"""

with open("input.txt") as f:
    data = f.read()

trees = [[int(c) for c in line.strip()] for line in data.splitlines()]


def countVisible(trees):
    top = [0 for x in trees[0]]
    bottom = [0 for x in trees[0]]
    left = [0 for y in trees]
    right = [0 for y in trees]


def checkLeft(trees, row, column):
    value = trees[row][column]
    while column > 0:
        column -= 1
        if trees[row][column] >= value:
            return False
    return True


def checkRight(trees, row, column):
    value = trees[row][column]
    while column < len(trees[row]) - 1:
        column += 1
        if trees[row][column] >= value:
            return False
    return True


def checkUp(trees, row, column):
    value = trees[row][column]
    while row > 0:
        row -= 1
        if trees[row][column] >= value:
            return False
    return True


def checkDown(trees, row, column):
    value = trees[row][column]
    while row < len(trees) - 1:
        row += 1
        if trees[row][column] >= value:
            return False
    return True


visible_count = 0
row_range = len(trees)
column_range = len(trees[0])
for column in range(column_range):
    for row in range(row_range):
        if checkLeft(trees, row, column):
            visible_count += 1
        elif checkRight(trees, row, column):
            visible_count += 1
        elif checkUp(trees, row, column):
            visible_count += 1
        elif checkDown(trees, row, column):
            visible_count += 1

print(f"Part 1 : Total visible trees is {visible_count}")


def visibleLeft(trees, row, column):
    value = trees[row][column]
    visible = 0
    column -= 1
    while column >= 0:
        visible += 1
        if trees[row][column] >= value:
            break
        column -= 1
    return visible


def visibleRight(trees, row, column):
    value = trees[row][column]
    visible = 0
    column += 1
    while column < len(trees[row]):
        visible += 1
        if trees[row][column] >= value:
            break
        column += 1
    return visible


def visibleUp(trees, row, column):
    value = trees[row][column]
    visible = 0
    row -= 1
    while row >= 0:
        visible += 1
        if trees[row][column] >= value:
            break
        row -= 1
    return visible


def visibleDown(trees, row, column):
    value = trees[row][column]
    visible = 0
    row += 1
    while row < len(trees):
        visible += 1
        if trees[row][column] >= value:
            break
        row += 1
    return visible


def computeScenicScore(trees, row, column):
    return visibleLeft(trees, row, column) * visibleRight(trees, row, column) * visibleUp(trees, row, column) * visibleDown(trees, row, column)


highest_scenic_score = 0
for column in range(column_range):
    for row in range(row_range):
        score = computeScenicScore(trees, row, column)
        if score > highest_scenic_score:
            highest_scenic_score = score

print(f"Part 2 : Highest scenic score is {highest_scenic_score}")
