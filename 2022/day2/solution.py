data = """A Y
B X
C Z"""

with open("input.txt") as f:
    data = f.read()

THROW_VALUE = {
    "R": 1,
    "P": 2,
    "S": 3,
}

OPPONENT_MAP = {
    "A": "R",
    "B": "P",
    "C": "S",
}

SELF_MAP = {
    "X": "R",
    "Y": "P",
    "Z": "S",
}

SCORE_MAP = {
    "RR": 3,
    "RP": 0,
    "RS": 6,
    "PR": 6,
    "PP": 3,
    "PS": 0,
    "SR": 0,
    "SP": 6,
    "SS": 3,
}

OUTCOME_MAP = {
    "X": "L",
    "Y": "D",
    "Z": "W",
}

OUTCOME_THROW_MAP = {
    "RW": "P",
    "RL": "S",
    "RD": "R",
    "PW": "S",
    "PL": "R",
    "PD": "P",
    "SW": "R",
    "SL": "P",
    "SD": "S",
}


def score(me, opponent):
    return SCORE_MAP[me + opponent] + THROW_VALUE[me]


def scoreLine(line):
    opponent_raw, me_raw = line.split(' ')
    opponent = OPPONENT_MAP[opponent_raw]
    me = SELF_MAP[me_raw]
    return score(me, opponent)


def scoreLine2(line):
    opponent_raw, outcome_raw = line.split(' ')
    opponent = OPPONENT_MAP[opponent_raw]
    outcome = OUTCOME_MAP[outcome_raw]
    return score(OUTCOME_THROW_MAP[opponent + outcome], opponent)


lines = [line for line in data.split("\n")]
print(f"Day 1 total is {sum(scoreLine(line) for line in lines)}")
print(f"Day 2 score is {sum(scoreLine2(line) for line in lines)}")
