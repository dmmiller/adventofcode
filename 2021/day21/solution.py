from dataclasses import dataclass
data = """Player 1 starting position: 4
Player 2 starting position: 8"""

with open("input.txt") as f:
    data = f.read()


@dataclass
class Die:
    value: int
    rollCount: int

    def increment(self):
        self.rollCount += 1
        if self.value == 100:
            self.value = 1
        else:
            self.value += 1


@dataclass
class Player:
    position: int
    score: int

    def move(self, steps):
        for step in range(steps):
            if self.position == 10:
                self.position = 1
            else:
                self.position += 1
        self.score += self.position


p_1_position = int(data.splitlines()[0].split(" ")[-1])
p_2_position = int(data.splitlines()[1].split(" ")[-1])


die = Die(1, 0)
p_1 = Player(p_1_position, 0)
p_2 = Player(p_2_position, 0)
p_1_turn = True
turns = 0

while max(p_1.score, p_2.score) < 1000:
    move_count = 0
    for _ in range(3):
        move_count += die.value
        die.increment()
    move_count = move_count % 10
    if p_1_turn:
        p_1.move(move_count)
    else:
        p_2.move(move_count)
    p_1_turn = not p_1_turn

print(f"Part 1 : the score is {die.rollCount * min(p_1.score, p_2.score)}")
