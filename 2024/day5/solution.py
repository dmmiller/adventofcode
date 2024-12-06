data = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

with open("input.txt") as f:
  data = f.read()

rules, pagesRaw = data.split("\n\n")

previousMap : dict[int, set[int]] = {}
for rule in rules.splitlines():
  prior, after = map(int, rule.split("|"))
  if after not in previousMap:
    previousMap[after] = set()
  previousMap[after].add(prior)

pages : list[list[int]]= []
for page in pagesRaw.splitlines():
  pages.append(list(map(int, page.split(","))))


def isPageValid(page: list[int]) -> bool:
  priors : list[int] = []
  for i in range(len(page)):
    for p in priors:
      if page[i] not in previousMap:
         return False
      if p not in previousMap[page[i]]:
        return False
    priors.append(page[i])
  return True

def pageValue(page: list[int]) -> int:
  if not isPageValid(page):
    return 0
  return page[len(page) // 2]

def correctedPageValue(page: list[int]) -> int:
  if isPageValid(page):
    return 0

  numbers : set[int] = set(page)
  counter : dict[int, int] = {}
  for number in page:
    if number in previousMap:
      counter[number] = len(numbers & previousMap[number])
    else:
      counter[number] = 0

  newPage = sorted(page, key=lambda x: counter[x])
  return newPage[len(newPage) // 2]

print("Part 1 solution is ", sum(pageValue(page) for page in pages))
print("Part 2 solution is ", sum(correctedPageValue(page) for page in pages))