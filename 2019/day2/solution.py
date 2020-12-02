import sys
sys.path.append('/Users/dmiller/aoc')
from machine import Machine

file = open('input.txt')
initial_data = list(map(int, file.read().split(',')))
m = Machine()
m.load(initial_data)
m.update(1, 12)
m.update(2, 2)
m.run()
print("Part 1 result is ", m.get_memory_slot(0))

#Part 2
for noun in range(0, 100):
    for verb in range(0, 100):
        m.reset()
        m.load(initial_data)
        m.update(1, noun)
        m.update(2, verb)
        m.run()
        if m.get_memory_slot(0) == 19690720:
            print(100 * noun + verb)
            exit()