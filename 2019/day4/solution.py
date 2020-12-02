from collections import Counter

class PasswordValidator:
    def __init__(self, min : int, max : int):
        self.min = min
        self.max = max
        self.strict_mode = False

    def is_valid(self, password : int) -> bool:
        if password < self.min:
            return False
        if password > self.max:
            return False
        pwd = str(password)
        if len(pwd) != 6:
            return False
        if pwd[0] > pwd[1] or pwd[1] > pwd[2] or pwd[2] > pwd[3] or pwd[3] > pwd[4] or pwd[4] > pwd[5]:
            return False
        if pwd[0] != pwd[1] and pwd[1] != pwd[2] and pwd[2] != pwd[3] and pwd[3] != pwd[4] and pwd[4] != pwd[5]:
            return False
        if self.strict_mode:
            counts = Counter()
            for let in pwd:
                counts[let] += 1
            if 2 not in counts.values():
                return False
        return True

    def set_strict_mode(self, mode : bool) -> None:
        self.strict_mode = mode

validator = PasswordValidator(134792, 675810)
valid_count = 0
for p in range(134792, 675810):
    if validator.is_valid(p):
        valid_count += 1

print("Part 1 total valid count is ", valid_count)

validator.set_strict_mode(True)
valid_count = 0
for p in range(134792, 675810):
    if validator.is_valid(p):
        valid_count += 1

print("Part 2 total valid count is ", valid_count)

