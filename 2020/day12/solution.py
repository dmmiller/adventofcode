import re

direction_re = re.compile(r"(?P<action>\w)(?P<value>\d+)")

maps = {
    "N" : lambda x : (0, x),
    "E" : lambda x : (x, 0),
    "S" : lambda x : (0, -x),
    "W" : lambda x : (-x, 0),
}

def take2(current_x_boat, current_y_boat, current_x_waypoint, current_y_waypoint, line):
    match = direction_re.match(line)
    action, value = match["action"], int(match["value"])
    new_x_boat, new_y_boat, new_x_waypoint, new_y_waypoint = current_x_boat, current_y_boat, current_x_waypoint, current_y_waypoint
    if action in "NESW":
        delta_x_waypoint, delta_y_waypoint = maps[action](value)
        new_x_waypoint += delta_x_waypoint
        new_y_waypoint += delta_y_waypoint
    elif action == "F":
        delta_x_boat, delta_y_boat = value * current_x_waypoint, value * current_y_waypoint
        new_x_boat += delta_x_boat
        new_y_boat += delta_y_boat
    elif action in "RL":
        offset = int(value / 90)
        if action == "L":
            offset = 4 - offset
        if offset == 1:
            new_x_waypoint = current_y_waypoint
            new_y_waypoint = - current_x_waypoint
        elif offset == 2:
            new_x_waypoint = - current_x_waypoint
            new_y_waypoint = - current_y_waypoint
        elif offset == 3:
            new_x_waypoint = - current_y_waypoint
            new_y_waypoint = current_x_waypoint

    return new_x_boat, new_y_boat, new_x_waypoint, new_y_waypoint

def next(current_x, current_y, current_direction, line):
    match = direction_re.match(line)
    action, value = match["action"], int(match["value"])
    delta_x = 0
    delta_y = 0
    new_direction = current_direction
    if action in "NESW":
        delta_x, delta_y = maps[action](value)
    elif action == "F":
        delta_x, delta_y = maps[current_direction](value)
    elif action in "RL":
        index = "NESW".find(current_direction)
        offset = int(value / 90)
        if action == "L":
            offset = - offset
        new_direction = "NESW"[(index + offset) % 4]

    return current_x + delta_x, current_y + delta_y, new_direction


with open("input.txt") as f:
    lines = [line.strip() for line in f]

x, y, direction = 0, 0, "E"
for line in lines:
    x, y, direction = next(x, y, direction, line.strip())
print(f"Final location is ({x},{y}), with distance {abs(x) + abs(y)}")

x_boat, y_boat = 0, 0 
x_waypoint, y_waypoint = 10, 1
for line in lines:
    x_boat, y_boat, x_waypoint, y_waypoint = take2(x_boat, y_boat, x_waypoint, y_waypoint, line)
print(f"Final location in part 2 is ({x_boat},{y_boat}) with distance {abs(x_boat) + abs(y_boat)}")