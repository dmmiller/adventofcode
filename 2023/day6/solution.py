from dataclasses import dataclass
from functools import reduce

data = """Time:      7  15   30
Distance:  9  40  200"""

with open("input.txt") as f:
  data = f.read()


@dataclass
class Race:
  time: int
  distance: int

  def wins(self) -> int:
    count = 0
    for i in range(self.time):
      if (self.time - i) * i > self.distance:
        count += 1
    return count


time, distance = data.splitlines()
races: list[Race] = [Race(val[0], val[1]) for val in
                     zip(
    [int(t) for t in time.split(":")[1].strip().split(" ") if len(t) > 0],
    [int(d) for d in distance.split(":")[1].strip().split(" ") if len(d) > 0]
)]

part1 = reduce(lambda x, y: x*y.wins(), races, 1)
print("Part 1 solution is ", part1)

superRace = Race(int(time.split(":")[1].replace(" ", "")), int(
    distance.split(":")[1].replace(" ", "")))
print("Part 2 solution is ", superRace.wins())
