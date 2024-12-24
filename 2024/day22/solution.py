from collections import deque

data = """1
2
3
2024"""

with open("input.txt") as f:
  data = f.read()

buyers = [int(line) for line in data.splitlines()]

def generateSecretNumber(seed: int) -> int:
  def mix(a: int, b: int) -> int:
    return a ^ b

  def prune(a: int) -> int:
    return a % 16777216

  def step1(a: int) -> int:
    return prune(mix(a * 64, a))

  def step2(a: int) -> int:
    return prune(mix(a // 32, a))

  def step3(a: int) -> int:
    return prune(mix(a * 2048, a))

  return step3(step2(step1(seed)))

def genXSecretNumbers(seed: int, count: int) -> int:
  for _ in range(count):
    seed = generateSecretNumber(seed)
  return seed

print("Part 1 solution is ", sum(genXSecretNumbers(buyer, 2000) for buyer in buyers))

def getPriceChainMap(seed: int, count: int) -> dict[tuple[int, int, int, int], int]:
  result = {}
  chain = deque()
  previous = seed % 10
  for _ in range(count):
    seed = generateSecretNumber(seed)
    diff = (seed % 10) - previous
    chain.append(diff)
    previous = seed % 10
    if len(chain) > 4:
      chain.popleft()
    if len(chain) == 4:
      possible = (chain[0], chain[1], chain[2], chain[3])
      if possible not in result:
        result[possible] = seed % 10

  return result

def findMaxBananas(buyers: list[int]) -> int:
  chainMaps = [getPriceChainMap(buyer, 2000) for buyer in buyers]
  best = 0
  for a in range(-9, 10):
    for b in range(-9, 10):
      for c in range(-9, 10):
        for d in range(-9, 10):
          instruction = (a, b, c, d)
          value = sum(chainMap[instruction] if instruction in chainMap else 0 for chainMap in chainMaps)
          if value > best:
            best = value
  return best


print("Part 2 solution is ", findMaxBananas(buyers))