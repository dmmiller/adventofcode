data = """2333133121414131402"""

with open("input.txt") as f:
  data = f.read()

def computeChecksum(s: str) -> int:
  score = 0
  currentLeft = 0
  currentRight = len(s) - 1
  consumedLeft = 0
  consumedRight = 0
  virtualIndex = 0
  maxIndex = sum(int(c) for i, c in enumerate(s) if i % 2 == 0)

  while virtualIndex < maxIndex:
    leftValue = int(s[currentLeft])
    if consumedLeft == leftValue:
      consumedLeft = 0
      currentLeft += 1
      if int(s[currentLeft]) == 0:
        currentLeft += 1

    rightValue = int(s[currentRight])
    if consumedRight == rightValue:
      consumedRight = 0
      currentRight -= 2
      if int(s[currentRight]) == 0:
        currentRight -= 2

    if currentLeft % 2 == 0:
      # we are in a file
      score += (virtualIndex * (currentLeft // 2))
    else:
      # we are in free space
      score += (virtualIndex * (currentRight // 2))
      consumedRight += 1

    consumedLeft += 1
    virtualIndex += 1

  return score

def computeChecksum2(s: str) -> int:
  index = 0
  valueToIndexMap: dict[int, int] = {}
  valueToLengthMap: dict[int, int] = {}
  emptyMap: dict[int, list[int]] = {}
  for i, c in enumerate(s):
    value = int(c)
    if i % 2 == 0:
      valueToIndexMap[i // 2] = index
      valueToLengthMap[i // 2] = value
    else:
      if value not in emptyMap:
        emptyMap[value] = []
      emptyMap[value].append(index)
    index += value

  numberToMove = len(s) // 2
  while numberToMove > 0:
    spaceNeeded = valueToLengthMap[numberToMove]
    currentIndex = valueToIndexMap[numberToMove]
    leftMostIndex = currentIndex
    leftMostSize = 0
    for gap in range(9, spaceNeeded - 1, -1):
      if gap in emptyMap and len(emptyMap[gap]) > 0:
        if emptyMap[gap][0] < leftMostIndex:
          leftMostIndex = emptyMap[gap][0]
          leftMostSize = gap
    if leftMostIndex < currentIndex:
      gap = leftMostSize
      newIndex = emptyMap[gap][0]
      valueToIndexMap[numberToMove] = newIndex
      emptyMap[gap] = emptyMap[gap][1:]
      if spaceNeeded < gap:
        newGap = gap - spaceNeeded
        if newGap not in emptyMap:
          emptyMap[newGap] = []
        emptyMap[newGap].append(newIndex + spaceNeeded)
        emptyMap[newGap] = sorted(emptyMap[newGap])
    numberToMove -= 1

  total = 0
  for value, startIndex in valueToIndexMap.items():
    for i in range(valueToLengthMap[value]):
      total += value * (startIndex + i)
  return total


print("Part 1 solution is ", computeChecksum(data))
print("Part 2 solution is ", computeChecksum2(data))
