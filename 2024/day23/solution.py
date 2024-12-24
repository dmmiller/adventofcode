from itertools import combinations

data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

with open("input.txt") as f:
  data = f.read()

def buildMap(lines: str) -> dict[str, set[str]]:
  result: dict[str, set[str]] = {}
  for line in lines.splitlines():
    l, r = line.split("-")
    if l not in result:
      result[l] = set()
    if r not in result:
      result[r] = set()
    result[l].add(r)
    result[r].add(l)
  return result

def findConnectedThrees(connections: dict[str, set[str]]) -> set[tuple[str, str, str]]:
  results: set[tuple[str, str, str]] = set()
  for l, r in combinations(sorted(connections.keys()), 2):
    if l not in connections[r]:
      continue
    intersection = connections[l].intersection(connections[r])
    for node in intersection:
      if node > r:
        results.add((l, r, node))
  return results

def findWithTs(triples: set[tuple[str, str, str]]) -> int:
  return sum(1 if triple[0][0] == 't' or triple[1][0] == 't' or triple[2][0] == 't' else 0 for triple in triples)

connections = buildMap(data)
triples = findConnectedThrees(connections)
tCount = findWithTs(triples)

print("Part 1 solution is ", tCount)

