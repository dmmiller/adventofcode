import re
kvp_matcher = re.compile(r"(\S+):(\S+)")

class Passport:
    RequiredPropertyValidatorMap = {
        'byr' : lambda x: int(x) >= 1920 and int(x) <= 2002,
        'iyr' : lambda x: int(x) >= 2010 and int(x) <= 2020,
        'eyr' : lambda x: int(x) >= 2020 and int(x) <= 2030,
        'hgt' : lambda x: (len(x) == 4 or len(x) == 5) and ((x[-2:] == "in" and int(x[:-2]) >= 59 and int(x[:-2]) <= 76) or (x[-2:] == "cm" and int(x[:-2]) >= 150 and int(x[:-2]) <= 193)),
        'hcl' : lambda x: len(x) == 7 and x[0] == "#" and all(map(lambda y: y in "0123456789abcdef" , x[1:])),
        'ecl' : lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid' : lambda x: len(x) == 9 and all(map(lambda y: y in "0123456789" , x)),
    }

    OptionalProperties = [
        'cid',
    ]

    def __init__(self):
        self._properties = {}

    def addLine(self, line):
        kvpairs = map(lambda x: x.strip(), line.split(" "))
        for kvp in kvpairs:
            match = kvp_matcher.match(kvp)
            self._properties[match.group(1)] = match.group(2)

    def isValid(self):
        for prop in Passport.RequiredPropertyValidatorMap:
            if prop not in self._properties:
                return False
        return True

    def isDataValid(self):
        if not self.isValid():
            return False
        for prop in Passport.RequiredPropertyValidatorMap:
            if not Passport.RequiredPropertyValidatorMap[prop](self._properties[prop]):
                return False
        return True

file = open('input.txt')
lines = list(map(lambda x : x.strip(), file.readlines()))
index = 0
validCount = 0
dataValidCount = 0
while index < len(lines):
    passport = Passport()
    while index < len(lines) and lines[index] != "":
        passport.addLine(lines[index])
        index += 1
    index += 1
    validCount += 1 if passport.isValid() else 0
    dataValidCount += 1 if passport.isDataValid() else 0

print("Found", validCount, "valid passports")
print("Found", dataValidCount, "data valid passports")
