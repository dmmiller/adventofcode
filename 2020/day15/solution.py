from __future__ import  annotations

input = [15,5,1,4,7,0]

def find_nth_number(starting : list[int], nth : int) -> int:
    last_spoken = { value : [index] for index, value in enumerate(starting)}
    round = len(starting)
    last_number = starting[-1]
    while round < nth:
        if len(last_spoken[last_number]) == 1:
            last_number = 0
        elif len(last_spoken[last_number]) == 2:
            penultimate, ultimate = last_spoken[last_number]
            last_number = ultimate - penultimate
        else:
            print("OOPS")
            return -1
        if last_number not in last_spoken:
            last_spoken[last_number] = []
        last_spoken[last_number].append(round)
        last_spoken[last_number] = last_spoken[last_number][-2:]
        round += 1
    return last_number

number = find_nth_number(input, 2020)
print(f"The 2020th number is {number}")
number = find_nth_number(input, 30000000)
print(f"The 30000000th number is {number}")