example = """2199943210
3987894921
9856789892
8767896789
9899965678"""

with open("input.txt") as f:
    values = [[int(val) for val in line.strip()] for line in f.readlines()]
#    values = [[int(val) for val in line.strip()] for line in example.split("\n")]
height = len(values)
length = len(values[0])
low_points = []
for h in range(height):
    for l in range(length):
        value = values[h][l]
        if h - 1 >= 0 and values[h-1][l] <= value:
            continue
        elif l - 1 >= 0 and values[h][l-1] <= value:
            continue
        elif h + 1 < height and values[h+1][l] <= value:
            continue
        elif l + 1 < length and values[h][l+1] <= value:
            continue
        low_points.append((h,l))
print(f"Part 1 sum of lows is {sum(values[low[0]][low[1]] + 1 for low in low_points)}")

basin_grid = {(y,x) : (y,x) for y in range(height) for x in range(length)}
changed = True
while changed:
    changed = False
    for h in range(height):
        for l in range(length):
            if values[h][l] == 9:
                continue
            ref_h, ref_l = basin_grid[(h,l)]
            ref_value = values[ref_h][ref_l]
            if 0 <= ref_h - 1 and values[ref_h - 1][ref_l] < ref_value:
                basin_grid[(h,l)] = (ref_h - 1, ref_l)
                changed = True
            elif 0 <= ref_l - 1 and values[ref_h][ref_l - 1] < ref_value:
                basin_grid[(h,l)] = (ref_h, ref_l - 1)
                changed = True
            if ref_h + 1 < height and values[ref_h + 1][ref_l] < ref_value:
                basin_grid[(h,l)] = (ref_h + 1, ref_l)
                changed = True
            elif ref_l + 1 < length and values[ref_h][ref_l + 1] < ref_value:
                basin_grid[(h,l)] = (ref_h, ref_l + 1)
                changed = True

basin_sizes = [sum(1 for val in basin_grid.values() if val == low) for low in low_points]
basin_sizes = sorted(basin_sizes, reverse=True)
print(f"Part 2 product of 3 largest basins is {basin_sizes[0] * basin_sizes[1] * basin_sizes[2]}")