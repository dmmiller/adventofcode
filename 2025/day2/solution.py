data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

with open("input.txt") as f:
  data = f.read()

def isPart1InvalidSum(s):
  if len(s) % 2 != 0:
    return False
  if s[:len(s)//2] == s[len(s)//2:]:
    return True
  return False

def isPart2InvalidSum(s):
  length = len(s)
  for chunkSize in range(1, length // 2 + 1):
    if length % chunkSize == 0:
      chunks = length // chunkSize
      valid = True
      for i in range(0, chunkSize):
        base = s[i]
        for j in range(1, chunks):
          if s[i + (j * chunkSize)] != base:
            valid = False
            break
      if valid:
        return True
  return False

part1InvalidSum = 0
part2InvalidSum = 0
maxLen = 0
for r in data.split(","):
  parts = r.split("-")
  start = int(parts[0])
  end = int(parts[1])
  for i in range(start, end + 1):
    s = str(i)
    if len(s) > maxLen:
      maxLen = len(s)
    if isPart1InvalidSum(s):
      part1InvalidSum += i
    if isPart2InvalidSum(s):
      part2InvalidSum += i

print("Part 1 solution is ", part1InvalidSum)
print("Part 2 solution is ", part2InvalidSum)