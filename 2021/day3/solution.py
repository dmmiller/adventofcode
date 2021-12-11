with open("input.txt") as f:
    numbers = [x.strip() for x in f.readlines()]
bit_count = len(numbers[0])
gamma = ""
epsilon = ""
for i in range(bit_count):
    bits_1 = sum(1 for n in numbers if n[i] == "1")
    bits_0 = sum(1 for n in numbers if n[i] == "0")
    if bits_1 > bits_0:
        gamma += "1"
        epsilon += "0"
    else:
        gamma += "0"
        epsilon += "1"

print("Part 1")
print(f"Gamma * Epsilon = {int(gamma, 2) * int(epsilon,2)}")

oxygen_potentials = [x for x in numbers]
bit_index = 0
while len(oxygen_potentials) > 1:
    bits_1 = sum(1 for x in oxygen_potentials if x[bit_index] == "1")
    bits_0 = sum(1 for x in oxygen_potentials if x[bit_index] == "0")
    if bits_1 > bits_0:
        oxygen_potentials = [x for x in oxygen_potentials if x[bit_index] == "1"]
    elif bits_1 < bits_0:
        oxygen_potentials = [x for x in oxygen_potentials if x[bit_index] == "0"]
    elif bits_1 == bits_0:
        oxygen_potentials = [x for x in oxygen_potentials if x[bit_index] == "1"]
    bit_index += 1

co2_potentials = [x for x in numbers]
bit_index = 0
while len(co2_potentials) > 1:
    bits_1 = sum(1 for x in co2_potentials if x[bit_index] == "1")
    bits_0 = sum(1 for x in co2_potentials if x[bit_index] == "0")
    if bits_1 > bits_0:
        co2_potentials = [x for x in co2_potentials if x[bit_index] == "0"]
    elif bits_1 < bits_0:
        co2_potentials = [x for x in co2_potentials if x[bit_index] == "1"]
    elif bits_1 == bits_0:
        co2_potentials = [x for x in co2_potentials if x[bit_index] == "0"]
    bit_index += 1
print("Part 2")
print(f"O2 * CO2 = {int(oxygen_potentials[0],2) * int(co2_potentials[0],2)}")