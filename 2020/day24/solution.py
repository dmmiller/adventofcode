from __future__ import annotations
from enum import Enum
from typing import Iterable, Iterator

import time

class Direction(Enum):
    NE = 1
    E = 2
    SE = 3
    SW = 4
    W = 5
    NW = 6

# Cube Coordinates from https://www.redblobgames.com/grids/hexagons/
HexCoordinate = tuple[int, int, int]
HexGrid = dict[HexCoordinate, bool]

DIRECTION_MAP = {
    'ne' : Direction.NE,
    'e' : Direction.E,
    'se' : Direction.SE,
    'sw' : Direction.SW,
    'w' : Direction.W,
    'nw' : Direction.NW,
}

HEX_OFFSETS = [(-1, 0, 1), (-1, 1, 0), (0, -1, 1), (0, 1, -1), (1, -1, 0), (1, 0, -1)]

def yield_directions(line: str) -> Iterator[Direction]:
    i = 0
    while i < len(line):
        if line[i] == 'e' or line[i] == 'w':
            yield DIRECTION_MAP[line[i]]
        else:
            yield DIRECTION_MAP[line[i:i+2]]
            i += 1
        i += 1

def follow_path(path: Iterable[Direction]) -> HexCoordinate:
    point = (0, 0, 0)
    for direction in path:
        if direction == Direction.NE:
            point = (point[0] + 1, point[1], point[2] - 1)
        elif direction == Direction.E:
            point = (point[0] + 1, point[1] - 1, point[2])
        elif direction == Direction.SE:
            point = (point[0], point[1] - 1, point[2] + 1)
        elif direction == Direction.SW:
            point = (point[0] - 1, point[1], point[2] + 1)
        elif direction == Direction.W:
            point = (point[0] - 1, point[1] + 1, point[2])
        elif direction == Direction.NW:
            point = (point[0], point[1] + 1, point[2] - 1)
    return point

def build_grid(paths: Iterable[Iterable[Direction]]) -> HexGrid:
    tiles = {}
    for path in paths:
        point = follow_path(path)
        if point in tiles:
            tiles[point] = not tiles[point]
        else:
            tiles[point] = True
    return tiles

def count_black_tiles(grid: HexGrid) -> int:
    return sum(1 for k, v in grid.items() if v)

def yield_neighbors(point: HexCoordinate) -> Iterable[HexCoordinate]:
    for offset in HEX_OFFSETS:
        yield (point[0] + offset[0], point[1] + offset[1], point[2] + offset[2])

def next_generation(grid: HexGrid) -> HexGrid:

    def active_count(point: HexCoordinate) -> int:
        return sum(
            1 for offset in HEX_OFFSETS
            if (point[0] + offset[0], point[1] + offset[1], point[2] + offset[2]) in grid and grid[(point[0] + offset[0], point[1] + offset[1], point[2] + offset[2])] == True
        )

    seen = set()
    new_grid = {}
    for point in grid:
        for neighbor in yield_neighbors(point):
            if neighbor in seen:
                continue
            seen.add(neighbor)
            neighbor_count = active_count(neighbor)
            new_value = grid[neighbor] if neighbor in grid else False
            if neighbor in grid and grid[neighbor] == True and (neighbor_count == 0 or neighbor_count > 2):
                new_value = False
            elif neighbor_count == 2 and (neighbor not in grid or grid[neighbor] == False):
                new_value = True
            if new_value:
                new_grid[neighbor] = new_value

    return new_grid

with open('input.txt') as f:
    paths = [yield_directions(line.strip()) for line in f.readlines()]

tiles = build_grid(paths)
print(f"Part 1 : Total black tiles is {count_black_tiles(tiles)}")

for i in range(100):
    tiles = next_generation(tiles)
print(f"Part 2 : Black tile count after 100 days is {count_black_tiles(tiles)}")