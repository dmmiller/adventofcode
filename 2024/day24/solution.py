from operator import xor, and_, or_
from typing import Callable
from functools import cache

data = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

with open("input.txt") as f:
  data = f.read()

def buildWiresAndGates(input: str) -> tuple[dict[str, int], dict[str, tuple[str, str, Callable[[int, int], int]]]] :
  wires: dict[str, int] = {}
  gates: dict[str, tuple[str, str, Callable[[int, int], int]]] = {}

  wireData, gateInfo = input.split("\n\n")
  for wireLine in wireData.splitlines():
    wire, value = wireLine.split(": ")
    wires[wire] = int(value)

  for gateLine in gateInfo.splitlines():
    operation, wire = gateLine.split(" -> ")
    l, op, r = operation.split(" ")
    func = xor
    if op == "AND":
      func = and_
    elif op == "OR":
      func = or_
    gates[wire] = (l, r, func)

  return (wires, gates)


def combineZs(wires: dict[str, int], gates: dict[str, tuple[str, str, Callable[[int, int], int]]]) -> int:

  @cache
  def resolve(wire: str) -> int:
    if wire in wires:
      return wires[wire]
    l, r, f = gates[wire]
    return f(resolve(l), resolve(r))

  zWires = sum(1 if k[0] == 'z' else 0 for k in gates.keys())
  value = 0
  for i in range(zWires):
    bit = resolve(f"z{i:02d}")
    if bit == 1:
      value += pow(2, i)
  return value

wires, gates = buildWiresAndGates(data)
print("Part 1 solution is ", combineZs(wires, gates))