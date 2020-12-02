import sys
sys.path.append('/Users/dmiller/aoc')
from machine import Machine

file = open('input.txt')
initial_data = list(map(int, file.read().split(',')))

print('Starting Part 1 diagnostics')
m = Machine()
m.load(initial_data)
m.set_input(1)
m.run()
print('Done with Part 1 diagnostics with output ', m.get_output())


print('Starting Part 2')
m.reset()
m.load(initial_data)
m.set_input(5)
m.run()
print('Done with Part 2 with output ', m.get_output())
