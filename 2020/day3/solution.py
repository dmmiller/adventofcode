file = open('input.txt')

class grid:
    
    def __init__(self, lines):
        self.lines = list(lines)

    def isTree(self, x, y):
        if y > self.height():
            return False
        row = self.lines[self.height() - y]
        while x > len(row):
            x -= len(row)
        if row[x-1] == '#':
            return True
        return False

    def height(self):
        return len(self.lines)


grid = grid(map(lambda x: x.strip(), file.readlines()))

def treeCountWithSlope(grid, right, down):
    x = 1
    y = grid.height()
    treeCount = 0
    while y > 0:
        treeCount += 1 if grid.isTree(x, y) else 0
        x += right
        y -= down
    return treeCount

partOne = treeCountWithSlope(grid, 3, 1)
print("The sleight hits ", partOne, "trees")

partTwoSlopeOne = treeCountWithSlope(grid, 1, 1)
partTwoSlopeTwo = treeCountWithSlope(grid, 3, 1)
partTwoSlopeThree = treeCountWithSlope(grid, 5, 1)
partTwoSlopeFour = treeCountWithSlope(grid, 7, 1)
partTwoSlopeFive = treeCountWithSlope(grid, 1, 2)

print("The multiplied Tree Count is ", partTwoSlopeOne * partTwoSlopeTwo * partTwoSlopeThree * partTwoSlopeFour * partTwoSlopeFive)
