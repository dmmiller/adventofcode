data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

data = """11111
99991
11911
19919
11111"""

with open("input.txt") as f:
    data = f.read()
grid = [[int(v) for v in line] for line in data.split("\n")]

def compute_risk_level(risks):
    risk_height = len(risks)
    risk_width = len(risks[0])

    risklevels = [[None for i in range(risk_width)] for j in range(risk_height)]

    def compute_min_risk(h, w):
        values = []
        if 0 <= h < risk_height and 0 <= w - 1 < risk_width and risklevels[h][w-1] != None:
            values.append(risklevels[h][w-1])
        if 0 <= h < risk_height and 0 <= w + 1 < risk_width and risklevels[h][w+1] != None:
            values.append(risklevels[h][w+1])
        if 0 <= h-1 < risk_height and 0 <= w < risk_width and risklevels[h-1][w] != None:
            values.append(risklevels[h-1][w])
        if 0 <= h+1 < risk_height and 0 <= w < risk_width and risklevels[h+1][w] != None:
            values.append(risklevels[h+1][w])
        return min(values) + risks[h][w]

    risklevels[0][0] = 0
    for x in range(1, risk_width):
        risklevels[0][x] = risklevels[0][x-1] + risks[0][x]
    for y in range(1, risk_height):
        risklevels[y][0] = risklevels[y - 1][0] + risks[y][0]

    for h in range(1, risk_height):
        for w in range(1, risk_width):
            risklevels[h][w] = compute_min_risk(h,w)

    changed = True
    while changed:
        changed = False
        for h in range(0, risk_height):
            for w in range(0, risk_width):
                min_risk_level = compute_min_risk(h,w)
                if risklevels[h][w] > min_risk_level:
                    changed = True
                    risklevels[h][w] = min_risk_level
                    
    return risklevels[-1][-1]

print(f"Part 1, smallest total risk is {compute_risk_level(grid)}")

def get_offset_value(current, offset):
    if current + offset > 9:
        return current + offset - 9
    return current + offset

grid_height = len(grid)
grid_width = len(grid[0])
big_grid_muliplier = 5
big_grid = [[None for i in range(big_grid_muliplier * grid_width)] for j in range(big_grid_muliplier * grid_width)]
for i in range(big_grid_muliplier):
    for j in range(big_grid_muliplier):
        for h in range(grid_height):
            for w in range(grid_width):
                big_grid[i*grid_height + h][j*grid_width + w] = get_offset_value(grid[h][w], i + j)
print(f"Part 2, smallest risk is {compute_risk_level(big_grid)}")
