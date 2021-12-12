from collections import deque
from typing import Counter

example = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

caves = {}
with open("input.txt") as f:
    for line in f.readlines():
#    for line in example.split("\n"):
        a, b = line.strip().split("-")
        if a not in caves:
            caves[a] = []
        caves[a].append(b)
        if b not in caves:
            caves[b] = []
        caves[b].append(a)

def find_paths(caves):
    start = caves['start']
    complete_paths = []
    potential_paths = deque()
    initial_path = deque()
    initial_path.append('start')
    potential_paths.append(initial_path)
    while len(potential_paths) > 0:
        path = potential_paths.popleft()
        for connection in caves[path[len(path) - 1]]:
            if connection.islower() and connection in path:
                continue
            path.append(connection)
            if connection == 'end':
                complete_paths.append(path.copy())
            else:
                potential_paths.append(path.copy())
            path.pop()
    return complete_paths

paths = find_paths(caves)
print(f"Part 1 : path count is {len(paths)}")

def find_paths_2(caves):
    start = caves['start']
    complete_paths = []
    potential_paths = deque()
    initial_path = deque()
    initial_path.append('start')
    potential_paths.append(initial_path)
    while len(potential_paths) > 0:
        path = potential_paths.popleft()
        for connection in caves[path[len(path) - 1]]:
            if connection.islower():
                if connection == 'start':
                    continue
                lowercount = Counter(cave for cave in path if cave.islower())
                if sum(lowercount.values()) > len(lowercount)+1:
                    continue
            path.append(connection)
            if connection == 'end':
                complete_paths.append(path.copy())
            else:
                potential_paths.append(path.copy())
            path.pop()
    return complete_paths

paths = find_paths_2(caves)
print(f"Part 2 : path count is {len(paths)}")