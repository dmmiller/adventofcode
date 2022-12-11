from dataclasses import dataclass, field
from math import prod
from typing import Callable
import re

data = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

with open("input.txt") as f:
    data = f.read()


@dataclass
class Monkey:
    number: int
    operation: Callable[[int], int]
    divisibilityValue: int
    true: int
    false: int
    items: list[int] = field(default_factory=list)
    itemsInspected: int = 0

    def inspectItems(self, monkeys, worryAdjustment):
        for item in self.items:
            self.itemsInspected += 1
            item = self.operation(item)
            item = worryAdjustment(item)
            if item % self.divisibilityValue == 0:
                monkeys[self.true].items.append(item)
            else:
                monkeys[self.false].items.append(item)
        self.items = []

    def adjustWorryPart1(item: int) -> int:
        return item // 3


id_re = re.compile(r"Monkey (?P<id>\d+):")
starting_items_re = re.compile(r"\s+Starting items: (?P<items>.*)")
operation_re = re.compile(r"\s+Operation: new = (?P<formula>.*)")
test_re = re.compile(r"\s+Test: divisible by (?P<divisor>\d+)")
true_re = re.compile(r"\s+If true: throw to monkey (?P<monkey>\d+)")
false_re = re.compile(r"\s+If false: throw to monkey (?P<monkey>\d+)")


def parseMonkey(s: str) -> Monkey:

    def buildLambda(formula: str) -> Callable[[int], int]:
        return lambda old: eval(formula, None, {"old": old})

    id_line, starting_items_line, operation_line, test_line, true_line, false_line = s.splitlines()
    id = int(id_re.match(id_line)['id'])
    starting_items = [int(item) for item in starting_items_re.match(
        starting_items_line)['items'].split(", ")]
    operation = buildLambda(operation_re.match(operation_line)['formula'])
    test = int(test_re.match(test_line)['divisor'])
    true = int(true_re.match(true_line)['monkey'])
    false = int(false_re.match(false_line)['monkey'])
    return Monkey(id, operation, test, true, false, starting_items)


def monkeyBusiness(monkeys: list[Monkey]) -> int:
    sorted_monkeys = sorted(
        monkeys, key=lambda m: m.itemsInspected, reverse=True)
    return sorted_monkeys[0].itemsInspected * sorted_monkeys[1].itemsInspected


monkeys = [parseMonkey(line) for line in data.split("\n\n")]

for round in range(20):
    for monkey in monkeys:
        monkey.inspectItems(monkeys, worryAdjustment=Monkey.adjustWorryPart1)

print(
    f"Part 1 : The product of two most active monkeys is {monkeyBusiness(monkeys)}")

# Reset data for part 2
monkeys = [parseMonkey(line) for line in data.split("\n\n")]
least_common_multiple = prod(monkey.divisibilityValue for monkey in monkeys)

for round in range(10000):
    for monkey in monkeys:
        monkey.inspectItems(monkeys, worryAdjustment=lambda x: x %
                            least_common_multiple)

print(
    f"Part 1 : The product of two most active monkeys is {monkeyBusiness(monkeys)}")
