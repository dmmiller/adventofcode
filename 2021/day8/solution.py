raw = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

with open("input.txt") as f:
    lines = [line.strip() for line in f.readlines()]
#    lines = [line.strip() for line in raw.split("\n")]

unique_count = 0
for line in lines:
    output = [digit.strip() for digit in line.split("|")[1].split(" ") if len(digit) > 0]
    unique_count += sum([1 for x in output if len(x) in [2,3,4,7]])
print(f"Part 1 {unique_count}")

def findOutput(line: str) -> int:
    input, output = line.split("|")
    def canonicalize(s):
        return [set(digit.strip()) for digit in s.split(" ") if len(digit.strip()) > 0]
    input = canonicalize(input)
    output = canonicalize(output)
    digits_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in input:
        if len(i) == 2:
            digits_array[1] = i
        elif len(i) == 3:
            digits_array[7] = i
        elif len(i) == 4:
            digits_array[4] = i
        elif len(i) == 7:
            digits_array[8] = i
    for i in input:
        if len(i) == 6:
            if digits_array[4] | digits_array[7] < i:
                digits_array[9] = i
            elif digits_array[7] < i:
                digits_array[0] = i
            else:
                digits_array[6] = i
        elif len(i) == 5:
            if digits_array[7] < i:
                digits_array[3] = i
            elif digits_array[4] - digits_array[1] < i:
                digits_array[5] = i
            else:
                digits_array[2] = i
    digits_map = {"".join(sorted(digit)): index for index, digit in enumerate(digits_array)}
    value = 0
    for digit in output:
        value = 10 * value + digits_map["".join(sorted(digit))]
    return value

print(f"Part 2 {sum(findOutput(line) for line in lines)}")