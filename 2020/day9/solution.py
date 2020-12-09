
def find_first_exception(numbers: list[int], lookback_count : int) -> int:
    window = set(numbers[:lookback_count])

    def window_sums_to_value(window, value):
        return any((value - x in window and value - x != x) for x in window)

    for i in range(lookback_count, len(numbers)):
        if not window_sums_to_value(window, numbers[i]):
            return numbers[i]
        window.remove(numbers[i - lookback_count])
        window.add(numbers[i])
    return -1

def find_weakness(numbers : list[int], key : int) -> int:
    l, r, total = 0, 0, 0
    while r < len(numbers):
        if total < key:
            total += numbers[r]
            r += 1
        elif total > key:
            total -= numbers[l]
            l += 1
        else:
            return min(numbers[l:r]) + max(numbers[l:r])    
    return -1

with open('input.txt') as f:
    numbers = [int(line.strip()) for line in f]
    key = find_first_exception(numbers, 25)
    print(f"First number that fails is {key}")
    weakness = find_weakness(numbers, key)
    print(f"The weakness is {weakness}")