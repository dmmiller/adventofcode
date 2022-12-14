from functools import cmp_to_key

data = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

with open("input.txt") as f:
    data = f.read()

pairs = [[eval(i) for i in pair.splitlines()] for pair in data.split("\n\n")]


def rightOrder(left, right):

    def check(l, r):
        i = 0
        while i < min(len(l), len(r)):
            if isinstance(l[i], int) and isinstance(r[i], int):
                if l[i] < r[i]:
                    return True
                elif l[i] > r[i]:
                    return False
            elif isinstance(l[i], list) and isinstance(r[i], list):
                result = check(l[i], r[i])
                if result != None:
                    return result
            else:
                if isinstance(l[i], int):
                    result = check([l[i]], r[i])
                else:
                    result = check(l[i], [r[i]])
                if result != None:
                    return result
            i += 1

        if len(l) == len(r):
            return None
        return len(l) < len(r)
    return check(left, right)


index_total = 0
for idx, pair in enumerate(pairs):
    if rightOrder(pair[0], pair[1]):
        index_total += (idx + 1)

print(f"Part 1 : The sum of indices in right order is {index_total}")


def comparison_function(l, r):
    result = rightOrder(l, r)
    if result:
        return -1
    if result == None:
        return 0
    return 1


all_items = [item for pair in pairs for item in pair]
divider_1 = [[2]]
divider_2 = [[6]]
all_items.append(divider_1)
all_items.append(divider_2)
sorted_items = sorted(all_items, key=cmp_to_key(comparison_function))

decoder_index = 1
for idx, item in enumerate(sorted_items):
    if item == divider_1 or item == divider_2:
        decoder_index *= (idx + 1)

print(f"Part 2 : The decoder index is {decoder_index}")
