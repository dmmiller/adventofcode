from __future__ import  annotations

def find_nth_number(starting: list[int], nth: int) -> int:
    last_spoken = {}
    next_number = 0
    gap = None
    for i in range(nth):
        if i < len(starting):
            next_number = starting[i]
        elif gap:
            next_number = gap
        else:
            next_number = 0

        if next_number in last_spoken:
            gap = i - last_spoken[next_number]
        else:
            gap = None
        last_spoken[next_number] = i
    return next_number

starting_sequence = [15,5,1,4,7,0]
number = find_nth_number(starting_sequence, 2020)
print(f"The 2020th number is {number}")
number = find_nth_number(starting_sequence, 30000000)
print(f"The 30000000th number is {number}")