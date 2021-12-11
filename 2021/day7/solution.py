example = "16,1,2,0,4,2,7,1,2,14"

with open("input.txt") as f:
    crabs = [int(val) for val in example.strip().split(",")]
    crabs = [int(val) for val in f.read().strip().split(",")]

min_fuel = max(crabs) * max(crabs)
for i in range(max(crabs)):
    fuel = 0
    for crab in crabs:
        fuel += abs(crab - i)
    if fuel < min_fuel:
        min_fuel = fuel
print(f"Part 1 - Minimum Fuel is {min_fuel}")

triangles = {0 : 0}
for i in range(1, max(crabs) + 1):
    triangles[i] = triangles[i - 1] + i

min_fuel = triangles[max(crabs)] * triangles[max(crabs)]
for i in range(max(crabs)):
    fuel = 0
    for crab in crabs:
        fuel += triangles[abs(crab - i)]
    if fuel < min_fuel:
        min_fuel = fuel
print(f"Part 2 - Minimum Fuel is {min_fuel}")
