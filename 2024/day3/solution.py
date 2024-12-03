import re
from itertools import chain

data = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

part1Pattern = re.compile(r"mul\((?P<op1>\d{1,3}),(?P<op2>\d{1,3})\)")
part2Pattern = re.compile(r"(do\(\))|(don't\(\))")
with open("input.txt") as f:
  data = f.read()


part1Matches = []
part2Matches = []
lineOffset = 0
for line in data.splitlines():
    matches = part1Pattern.finditer(line)
    enableMatches = part2Pattern.finditer(line)
    part1Matches.extend([lineOffset + match.start(), "mul", int(match.group("op1")), int(match.group("op2"))] for match in matches)
    part2Matches.extend([lineOffset + match.start(), match.end() - match.start() == 4] for match in enableMatches)
    lineOffset += len(line)

print("Part 1 solution is ", sum(match[2] * match[3] for match in part1Matches))
mergedMatches = sorted(chain(part1Matches, part2Matches), key=lambda x: x[0])
enabled = True
part2Solution = 0
for match in mergedMatches:
    if match[1] == "mul":
       if enabled:
          part2Solution += match[2] * match[3]
    else:
       enabled = match[1]
print("Part 2 solution is ", part2Solution)

