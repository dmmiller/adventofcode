from dataclasses import dataclass
from collections import deque


@dataclass
class Grid:
    height: int
    width: int
    data: list

    def getValue(self, x: int, y: int):
        assert x < self.width
        assert y < self.height
        return self.data[width * y + x]

    def setValue(self, x: int, y: int, value):
        assert x < self.width
        assert y < self.height
        self.data[width * y + x] = value


data = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

with open("input.txt") as f:
    data = f.read()

lines = data.splitlines()
width = len(lines[0])
height = len(lines)

data = data.replace("\n", "")
start_index = data.find("S")
end_index = data.find("E")

elevationGrid = Grid(height, width, data)
stepsGrid = Grid(height, width, [-1] * (height * width))
stepsGrid.data[end_index] = 0

end_x = end_index % width
end_y = end_index // width

work_queue = deque()
work_queue.append((end_x, end_y))


def elevation(c: str) -> int:
    if c == 'S':
        c = 'a'
    elif c == 'E':
        c = 'z'
    return ord(c) - ord('a')


while len(work_queue):
    current_x, current_y = work_queue.popleft()
    current_elevation = elevation(elevationGrid.getValue(current_x, current_y))
    current_steps = stepsGrid.getValue(current_x, current_y)
    for x_adjustment, y_adjustment in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_x = current_x + x_adjustment
        new_y = current_y + y_adjustment
        if 0 <= new_x < width and 0 <= new_y < height:
            new_elevation = elevation(elevationGrid.getValue(new_x, new_y))
            new_steps = stepsGrid.getValue(new_x, new_y)
            if new_steps == -1 and new_elevation + 1 >= current_elevation:
                stepsGrid.setValue(new_x, new_y, current_steps + 1)
                work_queue.append((new_x, new_y))

print(
    f"Part 1 : Number of steps from S to E is {stepsGrid.data[start_index]}")

min_so_far = stepsGrid.data[start_index]
for x in range(width):
    for y in range(height):
        if elevationGrid.getValue(x, y) == 'a':
            value = stepsGrid.getValue(x, y)
            if value != -1 and value < min_so_far:
                min_so_far = value

print(f"Part 2 : The fewest steps from elevation a to E is {min_so_far}")
