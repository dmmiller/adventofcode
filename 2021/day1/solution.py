

with open("input.txt") as f:
    depths = [int(line) for line in f.readlines()]

previous = 10000000
increases = 0
for depth in depths:
    if depth > previous:
        increases += 1
    previous = depth
print(f"Total depth increases {increases}")

previous = 1000000
increases = 0
for i in range(len(depths) - 2):
    window_total = depths[i] + depths[i+1] + depths[i+2]
    if window_total > previous:
        increases += 1
    previous = window_total

print(f"Total window depth increases {increases}")