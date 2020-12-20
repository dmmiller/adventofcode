from __future__ import annotations
from typing import IO, Generator
from math import sqrt
from functools import reduce
import re

tile_id_re = re.compile(r"Tile (?P<id>\d+):")

class Tile:

    def __init__(self, number: int, values: list[str]):
        self.number = number
        self.values = values
        self.rotation = 0

    def top(self) -> str:
        return self.values[0]

    def bottom(self) -> str:
        return self.values[-1]

    def left(self) -> str:
        return "".join(value[0] for value in self.values)
    
    def right(self) -> str:
        return "".join(value[-1] for value in self.values)

    def yield_edges(self) -> Generator[str, None, None]:
        top = self.top()
        yield top
        yield top[::-1]
        bottom = self.bottom()
        yield bottom
        yield bottom[::-1]
        right = self.right()
        yield right
        yield right[::-1]
        left = self.left()
        yield left
        yield left[::-1]

    def orient_to_match_left(self, pattern):
        if self.left() == pattern:
            return
        elif self.top() == pattern:
            self.reorient(3, True)
        elif self.right() == pattern:
            self.reorient(2, True)
        elif self.bottom() == pattern:
            self.reorient(1, False)
        elif self.left()[::-1] == pattern:
            self.reorient(0, True)
        elif self.top()[::-1] == pattern:
            self.reorient(3, False)
        elif self.right()[::-1] == pattern:
            self.reorient(2, False)
        elif self.bottom()[::-1] == pattern:
            self.reorient(1, True)
        if self.left() != pattern:
            print("ERROR in orient_to_match_left")

    def orient_to_match_right(self, pattern):
        if self.right() == pattern:
            return
        elif self.top() == pattern:
            self.reorient(1, False)
        if self.right() != pattern:
            print("ERROR in orient_to_match_right")
    
    def orient_to_match_top(self, pattern):
        if self.top() == pattern:
            return
        elif self.right() == pattern:
            self.reorient(3, False)
        elif self.bottom() == pattern:
            self.reorient(0, True)
        elif self.left() == pattern:
            self.reorient(3, True)
        elif self.top()[::-1] == pattern:
            self.reorient(2, True)
        elif self.right()[::-1] == pattern:
            self.reorient(1, True)
        elif self.bottom()[::-1] == pattern:
            self.reorient(2, False)
        elif self.left()[::-1] == pattern:
            self.reorient(1, False)
        if self.top() != pattern:
            print("ERROR in orient_to_match_top")

    def reorient(self, rotations: int, flip: bool):
        size = len(self.values)
        new_values = [list(value) for value in self.values]
        if rotations % 4 == 1:
            for i in range(size):
                for j in range(size):
                    new_values[j][size - 1 - i] = self.values[i][j]
        elif rotations % 4 == 2:
            for i in range(size):
                for j in range(size):
                    new_values[size - 1 - i][size - 1 - j] = self.values[i][j]
        elif rotations % 4 == 3:
            for i in range(size):
                for j in range(size):
                    new_values[size - 1 - j][i] = self.values[i][j]
        if flip:
            for i in range(int(size / 2)):
                new_values[i], new_values[size - 1 - i] = new_values[size - 1 - i], new_values[i]
        self.values = ["".join(value) for value in new_values]


def yield_tile_strings(f: IO) -> Generator[list[str], None, None]:
    tile = []
    for line in f.readlines():
        line = line.strip()
        if line == "":
            yield tile
            tile = []
        else:
            tile.append(line)
    yield tile

def build_tile(tile: list[str]) -> Tile:
    tile_id = tile_id_re.match(tile[0])["id"]
    tile = tile[1:]
    return Tile(int(tile_id), tile)

def tiles_match(tile1: Tile, tile2: Tile) -> bool:
    return len(find_edge(tile1, tile2)) > 0

def find_edge(tile1: Tile, tile2: Tile) -> str:
    tile1_top = tile1.top()
    tile1_bottom = tile1.bottom()
    tile1_right = tile1.right()
    tile1_left = tile1.left()

    for edge in tile2.yield_edges():
        if tile1_top == edge:
            return edge
        if tile1_bottom == edge:
            return edge
        if tile1_right == edge:
            return edge
        if tile1_left == edge:
            return edge
    return ''

def build_grid_map(tiles: list[Tile], matches: dict[int, set[int]]) -> list[list[int]]:
    grid_size = int(sqrt(len(tiles)))
    grid = []
    corners = [k for k, v in matches.items() if len(v) == 2]
    for i in range(grid_size):
        grid.append([])
        for j in range(grid_size):
            grid[i].append(None)
    grid[0][0] = corners[0]
    
    for i in range(1, grid_size):
        left = grid[0][i - 1]
        value = min(len(matches[match]) for match in matches[left])
        new = [match for match in matches[left] if len(matches[match]) == value][0]
        matches[left].remove(new)
        matches[new].remove(left)
        grid[0][i] = new

    for i in range(1, grid_size):
        for j in range(grid_size):
            above = grid[i - 1][j]
            new = matches[above].pop()
            matches[new].remove(above)
            if j > 0:
                left = grid[i][j - 1]
                matches[left].remove(new)
                matches[new].remove(left)
            grid[i][j] = new
    return grid

def build_grid(tile_map: dict[int, Tile], grid_array: list[list[int]]) -> list[str]:
    top_left_tile = tile_map[grid_array[0][0]]
    starting_edge = find_edge(top_left_tile, tile_map[grid_array[0][1]])
    top_left_tile.orient_to_match_right(starting_edge)
    left = top_left_tile.right()
    for i in range(1, len(grid_array)):
        tile = tile_map[grid_array[0][i]]
        tile.orient_to_match_left(left)
        left = tile.right()

    for i in range(1, len(grid_array)):
        for j in range(len(grid_array)):
            above = tile_map[grid_array[i - 1][j]]
            tile = tile_map[grid_array[i][j]]
            tile.orient_to_match_top(above.bottom())

    grid = []
    for grid_row in grid_array:
        for i in range(1, len(starting_edge) - 1):
            row = ""
            for tile_id in grid_row:
                row += tile_map[tile_id].values[i][1:-1]
            grid.append(row)
    return grid

def find_roughness(grid: list[str]) -> int:

    def yield_monster_rotations():
        monster_raw = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
        monster = [row for row in monster_raw.split('\n')]
        monster_points = [(r, c) for r, row in enumerate(monster) for c, char in enumerate(row) if char == '#']
        monster_width = max(c for r, c in monster_points)
        monster_height = max(r for r, c in monster_points)
        # four rotations
        for i in range(4):
            yield monster_height, monster_width, monster_points
            monster_points = [(c, monster_height - r) for r, c in monster_points]
            monster_height, monster_width = monster_width, monster_height
        # flip it
        monster_points = [(monster_height - r, c) for r, c in monster_points]
        # then 4 more rotations
        for i in range(4):
            yield monster_height, monster_width, monster_points
            monster_points = [(c, monster_height - r) for r, c in monster_points]
            monster_height, monster_width = monster_width, monster_height

    def monster_matches(h: int, w: int, monster_points: tuple[int, int]) -> bool:
        for r, c in monster_points:
            if grid[h + r][w + c] != "#":
                return False
        print(f"monster found at {h},{w}")
        return True

    match_count = 0
    for monster_height, monster_width, monster_points in yield_monster_rotations():
        for h in range(len(grid) - monster_height):
            for w in range(len(grid[h]) - monster_width):
                if monster_matches(h, w, monster_points):
                    match_count += 1
        if match_count != 0:
            break

    monster_bump_count = match_count * len(monster_points)
    hash_count = sum(sum(1 for c in row if c == "#") for row in grid)
    return hash_count - monster_bump_count


def build_adjacency_map(tiles: list[Tile]) -> dict[int, set[int]]:
    matches = {}
    for i in range(len(tiles)):
        matches[tiles[i].number] = set()
        for j in range(len(tiles)):
            if i == j:
                continue
            if tiles_match(tiles[i], tiles[j]):
                matches[tiles[i].number].add(tiles[j].number)
    return matches

with open('input.txt') as f:
    tiles = [build_tile(tile) for tile in yield_tile_strings(f)]
    adjacency_map = build_adjacency_map(tiles)
    corners = [k for k, v in adjacency_map.items() if len(v) == 2]
    print(f"The corners multiply to {reduce(lambda x, y: x * y, corners)}")
    grid_map = build_grid_map(tiles, adjacency_map)
    tile_map = { tile.number : tile for tile in tiles}
    grid = build_grid(tile_map, grid_map)
    roughness = find_roughness(grid)
    print(f"The roughness is {roughness}")