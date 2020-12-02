import re
password_re = re.compile(r"(\d+)-(\d+) (\w): (\w+)")

def parsePassword(line):
    match = password_re.match(line)
    return (int(match.group(1)), int(match.group(2)), match.group(3), match.group(4))

def isValidPartOne(minCount, maxCount, character, password):
    count = 0
    count = sum(1 if x == character else 0 for x in password)
    return count >= minCount and count <= maxCount

def isValidPartTwo(indexOne, indexTwo, character, password):
    countOne = 1 if password[indexOne - 1] == character else 0
    countTwo = 1 if password[indexTwo - 1] == character else 0
    return countOne + countTwo == 1

file = open('input.txt')
validPartOneCount = 0
validPartTwoCount = 0
for line in file.readlines():
    pwd = parsePassword(line)
    validPartOneCount += 1 if isValidPartOne(pwd[0], pwd[1], pwd[2], pwd[3]) else 0
    validPartTwoCount += 1 if isValidPartTwo(pwd[0], pwd[1], pwd[2], pwd[3]) else 0

print("Part 1 count is ", validPartOneCount)
print("Part 2 count is ", validPartTwoCount)

