from itertools import count

Point3D = tuple[int, int, int]
Point4D = tuple[int, int, int, int]
Space3D = dict[Point3D, str]
Space4D = dict[Point4D, str]

def build_cube(state: str) -> Space3D:
    return { (x,y,0) : value for y, line in zip(count(), state.split('\n')) for x, value in zip(count(), line.strip()) }

def build_hypercube(state: str) -> Space4D:
    return { (x,y,0,0) : value for y, line in zip(count(), state.split('\n')) for x, value in zip(count(), line.strip()) }

def next_generation(cube: Space3D) -> Space3D:

    def active_count(x: int, y: int, z: int) -> int:
        return sum(
            1 for x_ in range(x - 1, x + 2) 
            for y_ in range(y - 1, y + 2) 
            for z_ in range(z - 1, z + 2)
            if (x_, y_, z_) in cube and cube[(x_, y_, z_)] == "#" and not (x_ == x and y_ == y and z_ == z)
        )

    x_lo = min(map(lambda coord : coord[0], cube))
    x_hi = max(map(lambda coord : coord[0], cube))
    y_lo = min(map(lambda coord : coord[1], cube))
    y_hi = max(map(lambda coord : coord[1], cube))
    z_lo = min(map(lambda coord : coord[2], cube))
    z_hi = max(map(lambda coord : coord[2], cube))

    new_cube = {}
    for x in range(x_lo - 1, x_hi + 2):
        for y in range(y_lo - 1, y_hi + 2):
            for z in range(z_lo - 1, z_hi + 2):
                neighbor_count = active_count(x, y, z)
                new_value = "."
                if (x,y,z) in cube and cube[(x,y,z)] == "#" and 2 <= neighbor_count <= 3:
                    new_value = "#"
                elif neighbor_count == 3 and ((x,y,z) not in cube or cube[(x,y,z)] == "."):
                    new_value = "#"
                new_cube[(x,y,z)] = new_value
    return new_cube

def next_generation_hyper(cube: Space4D) -> Space4D:

    def active_count(x, y, z, w) -> int:
        return sum(
            1 for x_ in range(x - 1, x + 2) 
            for y_ in range(y - 1, y + 2) 
            for z_ in range(z - 1, z + 2)
            for w_ in range(w - 1, w + 2)
            if (x_, y_, z_, w_) in cube and cube[(x_, y_, z_, w_)] == "#" and not (x_ == x and y_ == y and z_ == z and w_ == w)
        )

    x_lo = min(map(lambda coord : coord[0], cube))
    x_hi = max(map(lambda coord : coord[0], cube))
    y_lo = min(map(lambda coord : coord[1], cube))
    y_hi = max(map(lambda coord : coord[1], cube))
    z_lo = min(map(lambda coord : coord[2], cube))
    z_hi = max(map(lambda coord : coord[2], cube))
    w_lo = min(map(lambda coord : coord[3], cube))
    w_hi = max(map(lambda coord : coord[3], cube))

    new_cube = {}
    for x in range(x_lo - 1, x_hi + 2):
        for y in range(y_lo - 1, y_hi + 2):
            for z in range(z_lo - 1, z_hi + 2):
                for w in range(w_lo - 1, w_hi + 2):
                    neighbor_count = active_count(x, y, z, w)
                    new_value = "."
                    if (x,y,z,w) in cube and cube[(x,y,z,w)] == "#" and 2 <= neighbor_count <= 3:
                        new_value = "#"
                    elif neighbor_count == 3 and ((x,y,z,w) not in cube or cube[(x,y,z,w)] == "."):
                        new_value = "#"
                    new_cube[(x,y,z,w)] = new_value
    return new_cube

initial_state = """.##.##..
..###.##
.##....#
###..##.
#.###.##
.#.#..#.
.......#
.#..#..#"""

cube = build_cube(initial_state)
hyper_cube = build_hypercube(initial_state)
for i in range(6):
    cube = next_generation(cube)
    hyper_cube = next_generation_hyper(hyper_cube)

print(f"Total number of active after six rounds is : {sum(1 for k, v in cube.items() if v == '#')}")
print(f"Total number of active hypercubes after six rounds is : {sum(1 for k, v in hyper_cube.items() if v == '#')}")