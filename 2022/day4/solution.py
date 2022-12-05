from dataclasses import dataclass

data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

with open("input.txt") as f:
    data = f.read()


@dataclass
class range:
    low: int
    high: int

    @staticmethod
    def parse(s: str):
        l, h = s.split('-')
        return range(int(l), int(h))

    def fullyContains(self, other):
        if self.low <= other.low and self.high >= other.high:
            return True
        return False

    def overlaps(self, other):
        if self.high < other.low:
            return False
        if self.low > other.high:
            return False
        return True


elf_pairs = [[range.parse(elf) for elf in line.split(',')]
             for line in data.splitlines()]

redundant_elf_count = sum(
    1 if left.fullyContains(right) or right.fullyContains(left) else 0
    for left, right in elf_pairs)

print(f"Part 1 : Fully contained elf count : {redundant_elf_count}")

overlap_elf_count = sum(
    1 if left.overlaps(right) else 0
    for left, right in elf_pairs)

print(f"Part 2 : Overlapping elf count : {overlap_elf_count}")
