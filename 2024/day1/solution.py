from collections import Counter

data = """3   4
4   3
2   5
1   3
3   9
3   3"""

with open("input.txt") as f:
  data = f.read()

list1 = []
list2 = []
for line in data.splitlines():
    locations = list(map(int, (x for x in line.split() if len(x) > 0)))
    list1.append(locations[0])
    list2.append(locations[1])
sortedlist1 = sorted(list1)
sortedlist2 = sorted(list2)
difference = sum(abs(pair[0] - pair[1]) for pair in zip(sortedlist1, sortedlist2))
print("Part 1 solution is ", difference)

counter1 = Counter(sortedlist1)
counter2 = Counter(sortedlist2)

similarityScore = 0
for k,v in counter1.items():
    if k in counter2:
        similarityScore += v * k * counter2[k]

print("Part 2 solution is ", similarityScore)