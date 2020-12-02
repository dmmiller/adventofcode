
def mass_to_fuel(mass):
    return int(mass / 3) - 2

def recursive_fuel(mass):
    fuel = mass_to_fuel(mass)
    total = 0
    while fuel >= 0:
        total += fuel
        fuel = mass_to_fuel(fuel)
    return total

total = 0
recursive_total = 0
file = open('input.txt')
for line in file.readlines():
    total += mass_to_fuel(int(line))
    recursive_total += recursive_fuel(int(line))

print("the total for part one is " + str(total))
print("the total for part 2 is " + str(recursive_total))