input = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

def line_of_sight(rows, r, c):

    def return_first_seat(r, c, delta_r, delta_c):
        r += delta_r
        c += delta_c        
        while 0 <= r < len(rows) and 0 <= c < len(rows[r]):
            if rows[r][c] != ".":
                return rows[r][c]
            r += delta_r
            c += delta_c
        return "."

    def count_occupied_neighbors(r, c):
        count = 0
        for delta_r in range(-1,2):
            for delta_c in range(-1,2):
                if not (delta_r == 0 and delta_c == 0):
                    count += 1 if return_first_seat(r, c, delta_r, delta_c) == "#" else 0
        return count

    if rows[r][c] == "L":
        if count_occupied_neighbors(r,c) == 0:
            return "#"
    elif rows[r][c] == "#":
        if count_occupied_neighbors(r,c) >= 5:
            return "L"
    return rows[r][c]

def adjacent(rows, r, c):

    def count_occupied_neighbors(r, c):
        count = 0
        for offset_r in range (-1, 2):
            for offset_c in range (-1, 2):
                if 0 <= r + offset_r < len(rows) and 0 <= c + offset_c < len(rows[r]) and (offset_r != 0 or offset_c != 0):
                    count += 1 if rows[r + offset_r][c + offset_c] == "#" else 0
        return count

    if rows[r][c] == "L":
        if count_occupied_neighbors(r,c) == 0:
            return "#"
    elif rows[r][c] == "#":
        if count_occupied_neighbors(r,c) >= 4:
            return "L"
    return rows[r][c]

def permute(rows, function):
    new_rows = []
    for r in range(len(rows)):
        new_row = ""
        for c in range(len(rows[r])):
            new_row += function(rows, r,c)
        new_rows.append(new_row)
    return new_rows

with open('input.txt') as f:
    original_rows = [line.strip() for line in f]
#original_rows = [line.strip() for line in input.split("\n")]
print(original_rows)
next_rows = []
previous_rows = original_rows
while True:
    next_rows = permute(previous_rows, adjacent)
    if next_rows == previous_rows:
        break
    previous_rows = next_rows
total = sum(1 if seat == "#" else 0 for row in next_rows for seat in row)
print(next_rows)
print(total)

print(original_rows)
previous_rows = original_rows
while True:
    next_rows = permute(previous_rows, line_of_sight)
    if next_rows == previous_rows:
        break
    previous_rows = next_rows
total = sum(1 if seat == "#" else 0 for row in next_rows for seat in row)
print(total)

