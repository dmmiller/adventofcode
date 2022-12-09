from collections import Counter

data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

with open("input.txt") as f:
    data = f.read()

head = (0, 0)
tail = (0, 0)
tail_visits = Counter()
tail_visits[tail] += 1


def adjustKnot(lead, follow):
    x_delta = lead[0] - follow[0]
    y_delta = lead[1] - follow[1]
    if abs(x_delta) > 1 or abs(y_delta) > 1:
        if x_delta:
            follow = (follow[0] + (1 if x_delta > 0 else -1), follow[1])
        if y_delta:
            follow = (follow[0], follow[1] + (1 if y_delta > 0 else -1))
        return (True, follow)
    return (False, follow)


for line in data.splitlines():
    x_change = 0
    y_change = 0
    step = 1
    match line.split():
        case ["R", value]:
            x_change = int(value)
        case ["L", value]:
            x_change = int(value)
            step = -1
        case ["U", value]:
            y_change = int(value)
        case ["D", value]:
            y_change = int(value)
            step = -1
        case _:
            print("not matched")
    for i in range(max(x_change, y_change)):
        head = (head[0] + (step if x_change else 0),
                head[1] + (step if y_change else 0))
        tail_moved, tail = adjustKnot(head, tail)
        if tail_moved:
            tail_visits[tail] += 1

print(f"Part 1 : The tail visits {len(tail_visits)} spots")

head = (0, 0)
knot_count = 9
knots = [(0, 0) for i in range(knot_count)]
tail_visits = Counter()
tail_visits[knots[knot_count - 1]] += 1

for line in data.splitlines():
    x_change = 0
    y_change = 0
    step = 1
    match line.split():
        case ["R", value]:
            x_change = int(value)
        case ["L", value]:
            x_change = int(value)
            step = -1
        case ["U", value]:
            y_change = int(value)
        case ["D", value]:
            y_change = int(value)
            step = -1
        case _:
            print("not matched")
    for i in range(max(x_change, y_change)):
        head = (head[0] + (step if x_change else 0),
                head[1] + (step if y_change else 0))
        tail_moved, knots[0] = adjustKnot(head, knots[0])
        for i in range(1, knot_count):
            if not tail_moved:
                break
            tail_moved, knots[i] = adjustKnot(knots[i - 1], knots[i])
            if i == knot_count - 1 and tail_moved:
                tail_visits[knots[knot_count - 1]] += 1

print(f"Part 2 : The tail visits {len(tail_visits)} spots")
