example = "3,4,3,1,2"
with open("input.txt") as f:
#    fish = [int(val) for val in example.strip().split(",")]
    fish = [int(val) for val in f.read().strip().split(",")]

fish_counter = [0,0,0,0,0,0,0,0,0]
for f in fish:
    fish_counter[f] += 1

for day in range(256):
    next_fish_counter = [0,0,0,0,0,0,0,0,0]
    for i in range(1, 9):
        next_fish_counter[i - 1] = fish_counter[i]
    next_fish_counter[6] += fish_counter[0]
    next_fish_counter[8] = fish_counter[0]
    fish_counter = next_fish_counter
    if day == 79:
        print(f"Part 1 - After 80 days : {sum(fish_counter)}")

print(f"Part 2 - After 256 days : {sum(fish_counter)}")