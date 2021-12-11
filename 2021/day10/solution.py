from enum import Enum

example = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

class LineClassification(Enum):
    VALID = 1
    INCOMPLETE = 2
    CORRUPT = 3


with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
#    lines = [line.strip() for line in example.split("\n")]

def classify(line):
    stack = []
    for c in line:
        if c in "([{<":
            stack.append(c)
        elif c in ")]}>":
            top = stack.pop()
            if (top == "(" and c == ')') or (top == "[" and c == ']') or (top == "{" and c == '}') or (top == "<" and c == '>'):
                continue
            else:
                return LineClassification.CORRUPT, c
        else:
            print("unknown character")
    if len(stack) > 0:
        return LineClassification.INCOMPLETE, stack
    return LineClassification.VALID, None

corruptionTable = {
    ')' : 3,
    ']' : 57,
    '}' : 1197,
    '>' : 25137,
}

def scoreCompletion(stack):
    score = 0
    scoreTable = {
        '(' : 1,
        '[' : 2,
        '{' : 3,
        '<' : 4,
    }
    while len(stack) > 0:
        value = stack.pop()
        score = 5 * score + scoreTable[value]
    return score

total_error = 0
completion_scores = []
for line in lines:
    classification, extra = classify(line)
    if classification == LineClassification.CORRUPT:
        total_error += corruptionTable[extra]
    elif classification == LineClassification.INCOMPLETE:
        completion_scores.append(scoreCompletion(extra))

print(f"Part 1 has a total error of {total_error}")
print(f"Part 2 has a middle completion score of {sorted(completion_scores)[int(len(completion_scores)/2)]}")
