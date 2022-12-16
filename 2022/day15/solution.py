import re
from dataclasses import dataclass
from typing import Tuple
from functools import reduce

data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

with open("input.txt") as f:
    data = f.read()


@dataclass
class Beacon:
    x: int
    y: int


@dataclass
class Sensor:
    x: int
    y: int
    closestBeacon: Beacon

    def distanceToBeacon(self):
        return abs(self.x - self.closestBeacon.x) + abs(self.y - self.closestBeacon.y)


line_re = re.compile(
    r"Sensor at x=(?P<s_x>-?\d+), y=(?P<s_y>-?\d+): closest beacon is at x=(?P<b_x>-?\d+), y=(?P<b_y>-?\d+)")

sensors = []
for line in data.splitlines():
    parsed_line = line_re.match(line)
    sensors.append(Sensor(int(parsed_line["s_x"]), int(parsed_line["s_y"]), Beacon(
        int(parsed_line["b_x"]), int(parsed_line["b_y"]))))


def generateNonBeaconsInRow(sensors: list[Sensor], row: int) -> Tuple[set[int],  set[int], set[int]]:
    elements_in_row = set()
    beacons_in_row = set()
    sensors_in_row = set()

    for s in sensors:
        if s.y == row:
            sensors_in_row.add(s.x)
        if s.closestBeacon.y == row:
            beacons_in_row.add(s.closestBeacon.x)
        if abs(s.y - row) < s.distanceToBeacon():
            x_range = s.distanceToBeacon() - abs(s.y - row)
            for x in range(-x_range, x_range+1):
                elements_in_row.add(s.x + x)

    return (elements_in_row, beacons_in_row, sensors_in_row)


def generateNonBeaconsInRowCount(sensors: list[Sensor], row: int) -> int:
    nonBeacons, beacons, sens = generateNonBeaconsInRow(sensors, row)
    return len(nonBeacons - beacons - sens)


def findDistressSignal(sensors: list[Sensor], size: int) -> int:

    def generateCandidates(sensor: Sensor) -> set[Tuple[int, int]]:
        distance = sensor.distanceToBeacon() + 1
        candidates = set()
        for y_offset in range(-distance, distance + 1):
            x_offset = distance - abs(y_offset)
            candidates.add((sensor.x + x_offset, sensor.y + y_offset))
            candidates.add((sensor.x - x_offset, sensor.y + y_offset))
        return candidates

    candidates = set()
    size += 1
    for s in sensors:
        candidates |= generateCandidates(s)

    for candidate in candidates:
        if 0 <= candidate[0] <= size and 0 <= candidate[1] <= size:
            for s in sensors:
                if abs(candidate[0] - s.x) + abs(candidate[1] - s.y) <= s.distanceToBeacon():
                    break
            else:
                return candidate[0] * 4000000 + candidate[1]

    return -1


print(
    f"Part 1 : Count of non beacons is {generateNonBeaconsInRowCount(sensors, 2000000)}")
# print(
#     f"Part 1 : Count of non beacons is {generateNonBeaconsInRowCount(sensors, 10)}")

sensors.sort(key=lambda s: s.y)

print(
    f"Part 2 : The distress signal is {findDistressSignal(sensors, 4000000)}")
# print(
#     f"Part 2 : The distress signal is {findDistressSignal(sensors, 20)}")
