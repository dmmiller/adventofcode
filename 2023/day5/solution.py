from dataclasses import dataclass, field
import sys
from itertools import islice

data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

with open("input.txt") as f:
  data = f.read()


@dataclass
class ConversionRange:
  destination: int
  source: int
  range: int


@dataclass
class Converter:
  ranges: list[ConversionRange] = field(default_factory=list)

  def convert(self, value: int) -> int:
    for r in self.ranges:
      if r.source <= value < r.source + r.range:
        return r.destination + (value - r.source)
    return value

  def invert(self, value: int) -> int:
    for r in self.ranges:
      if r.destination <= value < r.destination + r.range:
        return r.source + (value - r.destination)
    return value


seedString, *mapStrings = data.split("\n\n")

seeds: list[int] = [int(v)
                    for v in seedString.strip().split(":")[1].strip().split(" ")]

converters: list[Converter] = []
for mapString in mapStrings:
  ranges: list[ConversionRange] = []
  for rnge in mapString.strip().split("\n")[1:]:
    destination, source, range_ = map(int, rnge.strip().split(" "))
    ranges.append(ConversionRange(destination, source, range_))
  converters.append(Converter(ranges))

minLocation = 2**32
for seed in seeds:
  for converter in converters:
    seed = converter.convert(seed)
  if seed < minLocation:
    minLocation = seed

print("Part 1 solution is : ", minLocation)

seedPairs = []
iterator = iter(seeds)
while pair := list(islice(iterator, 2)):
  seedPairs.append(pair)

reversedConverters = [c for c in reversed(converters)]
minLocation = 2**32
for location in range(minLocation):
  original = location
  # if original % 1000000 == 0:
  #   print(original)
  done = False
  for converter in reversedConverters:
    location = converter.invert(location)
  for pair in seedPairs:
    if pair[0] <= location < pair[0] + pair[1]:
      done = True
      break
  if done:
    print("Part 2 solution is : ", original)
    break
