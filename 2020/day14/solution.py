from functools import reduce
import re

mask_re = re.compile(r"mask = (?P<value>\w{36})")
mem_re = re.compile(r"mem\[(?P<address>\d+)\] = (?P<value>\d+)")

def apply_value_mask(mask, value):
    mask_1s = int(mask.replace("X", "1"), base=2)
    mask_0s = int(mask.replace("X", "0"), base=2)
    return (value & mask_1s) | mask_0s

def apply_memory_mask(mask, value):
    bin_value = list('{0:036b}'.format(value))
    for i in range(len(mask)):
        if mask[i] == '1':
            bin_value[i] = '1'
        elif mask[i] == 'X':
            bin_value[i] = 'X'
    return ''.join(bin_value)

def generate_addresses(mask, address):
    def inner_generator(address):
        if 'X' not in address:
            yield int(address, base=2)
        else:
            for addr in inner_generator(address.replace("X", "0", 1)):
                yield addr
            for addr in inner_generator(address.replace("X", "1", 1)):
                yield addr

    address = apply_memory_mask(mask, address)
    for addr in inner_generator(address):
        yield addr

memory = {}
memory_2 = {}
with open('input.txt') as f:
    current_mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    for line in f.readlines():
        line = line.strip()
        if (mask_match := mask_re.match(line)):
            current_mask = mask_match['value']
        elif (mem_match := mem_re.match(line)):
            address, value = int(mem_match['address']), int(mem_match['value'])
            memory[address] = apply_value_mask(current_mask, value)
            for addr in generate_addresses(current_mask, address):
                memory_2[addr] = value

total = reduce(lambda x, y: x + y, memory.values())
print(f"Sum of all memory for Part 1 is {total}")
total = reduce(lambda x, y: x + y, memory_2.values())
print(f"Sum of all memory for Part 2 is {total}")
