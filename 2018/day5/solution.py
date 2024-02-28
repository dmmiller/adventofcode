from collections import deque

data = "dabAcCaCBAcCcaDA"

with open("input.txt") as f:
  data = f.read()

def computeLength(s: str) -> int:
    stack = deque()

    for c in s:
        if len(stack) == 0:
            stack.append(c)
        else:
            if abs(ord(c) - ord(stack[-1])) == 32:
                stack.pop()
            else:
                stack.append(c)
    return len(stack)

print("Part 1 : ", computeLength(data))

print("Part 2 : ", min((computeLength(data.replace(chr(i + ord("A")), "").replace(chr(i + ord("a")), "")) for i in range(26))))

