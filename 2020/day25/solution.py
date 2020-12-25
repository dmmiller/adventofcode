
def transform(subject: int, loop_size: int) -> int:
    value = 1
    for i in range(loop_size):
        value *= subject
        value = value % 20201227
    return value

def find_loop_size(public_key: int, subject: int) -> int:
    i = 0
    value = 1
    while value != public_key:
        value *= subject
        value = value % 20201227
        i += 1
    return i

# Example input
card_key = 5764801
door_key = 17807724
assert(transform(7, 8) == card_key)
assert(transform(7, 11) == door_key)
assert(transform(door_key, 8) == transform(card_key, 11))

assert(find_loop_size(card_key, 7) == 8)
assert(find_loop_size(door_key, 7) == 11)

# Real input
card_key = 9717666
door_key = 20089533

card_loop_size = find_loop_size(card_key, 7)
encryption_key = transform(door_key, card_loop_size)
print(f"The encryption key for part 1 is {encryption_key}")
