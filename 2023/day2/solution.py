from dataclasses import dataclass
import re

data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

with open("input.txt") as f:
  data = f.read()

round_re = re.compile(r"\s*(?P<count>\d+) (?P<color>blue|green|red),?")
game_re = re.compile(r"Game (?P<id>\d+)")


@dataclass
class Round:
  red: int = 0
  green: int = 0
  blue: int = 0

  @staticmethod
  def parse(s: str):
    red = 0
    blue = 0
    green = 0
    matches = round_re.findall(s.strip())
    for match in matches:
      count, color = match
      count = int(count)
      if color == "red":
        red = count
      elif color == "green":
        green = count
      elif color == "blue":
        blue = count
    return Round(red, green, blue)

  def possible(self, red, green, blue):
    return self.red <= red and self.green <= green and self.blue <= blue


@dataclass
class Game:
  id: int
  rounds: list[Round]

  def round1Possible(self):
    return all(round.possible(12, 13, 14) for round in self.rounds)

  def round2Power(self):
    redMax = max(round.red for round in self.rounds)
    greenMax = max(round.green for round in self.rounds)
    blueMax = max(round.blue for round in self.rounds)
    return redMax * greenMax * blueMax


def parseLine(s: str):
  gameString, roundsString = s.strip().split(":")
  rounds = [Round.parse(r) for r in roundsString.split(";")]
  id = int(game_re.match(gameString.strip()).group('id'))
  return Game(id, rounds)


games: list[Game] = []
for line in data.splitlines():
  games.append(parseLine(line))

part1Total = 0
part2Total = 0
for game in games:
  if game.round1Possible():
    part1Total += game.id
  part2Total += game.round2Power()

print("Part 1 solution is : ", part1Total)
print("Part 2 solution is : ", part2Total)
