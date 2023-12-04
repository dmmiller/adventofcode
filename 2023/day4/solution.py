from dataclasses import dataclass, field
from typing import Set

data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

with open("input.txt") as f:
  data = f.read()


@dataclass
class Card:
  id: int = 0
  winning: Set[int] = field(default_factory=set)
  have: Set[int] = field(default_factory=set)

  @staticmethod
  def parse(s: str):
    card, numbers = s.strip().split(":")
    id = int(card.strip().split(" ")[-1])
    winners, rest = numbers.strip().split("|")
    winning = set(int(c.strip())
                  for c in winners.strip().split(" ") if len(c.strip()) > 0)
    have = set(int(c.strip())
               for c in rest.strip().split(" ")if len(c.strip()) > 0)
    return Card(id, winning=winning, have=have)

  def points(self) -> int:
    count = self.winners()
    if count > 0:
      return pow(2, count - 1)
    return 0

  def winners(self) -> int:
    winners = self.winning.intersection(self.have)
    return len(winners)


cards: list[Card] = []
for line in data.splitlines():
  cards.append(Card.parse(line))

part1Total = 0
cardCounts: list[int] = [1 for card in cards]
for card in cards:
  part1Total += card.points()
  winners = card.winners()
  for w in range(winners):
    cardCounts[card.id + w] += cardCounts[card.id - 1]

print("Part 1 solution is : ", part1Total)
print("Part 2 solution is : ", sum(cardCounts))
