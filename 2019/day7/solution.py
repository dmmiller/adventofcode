import sys
sys.path.append('/Users/dmiller/aoc')
from amplifier import Amplifier
from itertools import permutations

file = open('input.txt')
initial_data = list(map(int, file.read().split(',')))

#initial_data = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#initial_data = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]

phase_permutations = permutations(range(5), 5)

print('Starting Part 1 diagnostics')
max_thrust = 0
for phases in phase_permutations:
    ampA = Amplifier(initial_data)
    ampA.set_phase(phases[0])
    ampA.set_input(0)
    ampA.run()
    ampB = Amplifier(initial_data)
    ampB.set_phase(phases[1])
    ampB.set_input(ampA.get_output())
    ampB.run()
    ampC = Amplifier(initial_data)
    ampC.set_phase(phases[2])
    ampC.set_input(ampB.get_output())
    ampC.run()
    ampD = Amplifier(initial_data)
    ampD.set_phase(phases[3])
    ampD.set_input(ampC.get_output())
    ampD.run()
    ampE = Amplifier(initial_data)
    ampE.set_phase(phases[4])
    ampE.set_input(ampD.get_output())
    ampE.run()
    if ampE.get_output() > max_thrust:
        max_thrust = ampE.get_output()
print('Done with Part 1 diagnostics with thrust ', max_thrust)


