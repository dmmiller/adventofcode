import re
from collections import Counter

line_re = re.compile(r"(?P<src>\d+,\d+) -> (?P<dest>\d+,\d+)")
lines = {}
raw = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
with open("input.txt") as f:
    for line in f.readlines():
#    for line in raw.split("\n"):
        m = line_re.match(line.strip())
        src = tuple(int(value) for value in m['src'].split(","))
        dest = tuple(int(value) for value in m['dest'].split(","))
        if src in lines:
            print("OOPS")
        lines[src] = dest

orthograph = Counter()
graph = Counter()
for src, dest in lines.items():
    if src[0] == dest[0]:
        ymin = min(src[1], dest[1])
        ymax = max(src[1], dest[1])
        for y in range(ymin, ymax+1):
            orthograph[src[0], y] += 1
            graph[src[0], y] += 1
    elif src[1] == dest[1]:
        xmin = min(src[0], dest[0])
        xmax = max(src[0], dest[0])
        for x in range(xmin, xmax+1):
            orthograph[x, src[1]] += 1
            graph[x, src[1]] += 1
    else:
        xstep = 1 if src[0] < dest[0] else -1
        ystep = 1 if src[1] < dest[1] else -1
        print(f"{src} -> {dest}")
        steps = abs(src[0] - dest[0])
        for i in range(steps + 1):
            x = src[0] + (i * xstep)
            y = src[1] + (i * ystep)
            graph[(x,y)] += 1

total_part1 = sum(1 for k,v in orthograph.items() if v > 1)
print(f"Total places with overlap {total_part1}")
total_part2 = sum(1 for k,v in graph.items() if v > 1)
print(f"Total for part 2 is {total_part2}")
