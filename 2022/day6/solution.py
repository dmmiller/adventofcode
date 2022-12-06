from collections import Counter

data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""

with open("input.txt") as f:
    data = f.read()


def findMarker(s: str, uniqueLength: int) -> int:
    counter = Counter(s[0:uniqueLength])
    index = uniqueLength
    while len(counter) != uniqueLength and index < len(s):
        removeIndex = index - uniqueLength
        counter[s[removeIndex]] -= 1
        counter[s[index]] += 1
        if (counter[s[removeIndex]] == 0):
            counter.pop(s[removeIndex])
        index += 1
    return index


def findStartOfPacketMarker(s: str) -> int:
    return findMarker(s, 4)


def findStartOfMessageMarker(s: str) -> int:
    return findMarker(s, 14)


print(f"Part 1 Start of packet Marker is {findStartOfPacketMarker(data)}")
print(f"Part 2 Start of message Marker is {findStartOfMessageMarker(data)}")
