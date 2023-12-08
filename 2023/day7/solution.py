from __future__ import annotations
from dataclasses import dataclass
from collections import Counter
from functools import cmp_to_key

data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

with open("input.txt") as f:
  data = f.read()

CardValues = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}

WildCardValues = {
    "J": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


@dataclass
class Hand:
  hand: str
  bet: int

  def value(self) -> int:
    return Hand.valueFromCounter(self.hand)

  def wildValue(self) -> int:
    counter = Counter(self.hand)
    jCount = counter["J"]
    if jCount == 0 or jCount == 5:
      return Hand.valueFromCounter(counter)
    del counter["J"]
    maxValue = max(counter.values())
    for k in counter.keys():
      if counter[k] == maxValue:
        counter[k] += jCount
        break

    return Hand.valueFromCounter(counter)

  @staticmethod
  def valueFromCounter(counter) -> int:
    if len(counter) == 1:
      # all the same - 5 of a kind
      return 7
    elif len(counter) == 2:
      # either 4 of a kind or a full house
      maxCount = max(counter.values())
      if maxCount == 4:
        return 6  # 4 of a kind
      return 5  # full house
    elif len(counter) == 3:
      # either 3 of kind or 2 pair
      maxCount = max(counter.values())
      if maxCount == 3:
        return 4  # 3 of a kind
      return 3  # 2 of a kind
    elif len(counter) == 4:
      # a pair
      return 2
    # all five are different
    return 1

  @staticmethod
  def compareHands(left: Hand, right: Hand) -> int:
    # return < 0 if left is less than right
    # return 0 if equal
    # return > 0 if left is greater than right
    lValue = left.value()
    rValue = right.value()

    if lValue != rValue:
      return lValue - rValue

    # compare individual cards
    for i in range(len(left.hand)):
      l = left.hand[i]
      r = right.hand[i]
      if l == r:
        continue
      return CardValues[l] - CardValues[r]
    return 0

  @staticmethod
  def compareWildHands(left: Hand, right: Hand) -> int:
    # return < 0 if left is less than right
    # return 0 if equal
    # return > 0 if left is greater than right
    lValue = left.wildValue()
    rValue = right.wildValue()

    if lValue != rValue:
      return lValue - rValue

    # compare individual cards
    for i in range(len(left.hand)):
      l = left.hand[i]
      r = right.hand[i]
      if l == r:
        continue
      return WildCardValues[l] - WildCardValues[r]
    return 0


hands = [Hand(values[0], int(values[1])) for line in data.splitlines() if (
    values := line.strip().split(" "))]


hands = sorted(hands, key=cmp_to_key(Hand.compareHands))
part1Total = 0
for i in range(len(hands)):
  part1Total += ((i + 1) * hands[i].bet)

print("Part 1 solution is ", part1Total)

hands = sorted(hands, key=cmp_to_key(Hand.compareWildHands))
part2Total = 0
for i in range(len(hands)):
  part2Total += ((i + 1) * hands[i].bet)

print("Part 2 solution is ", part2Total)
