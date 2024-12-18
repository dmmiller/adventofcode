import re

data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

with open("input.txt") as f:
  data = f.read()

data = """Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""

def buildInitialState(s: str) -> tuple[dict[str, int], list[int]]:
  registersRaw, programRaw = s.split("\n\n")
  registerRE = re.compile(r"Register (?P<register>[ABC]): (?P<value>\d+)")
  registers : dict[str, int] = {}
  for register in registersRaw.splitlines():
    m = registerRE.match(register)
    registers[m['register']] = int(m['value'])
  instructions = [int(number) for number in programRaw.split(":")[1].strip().split(",")]
  return (registers, instructions)

def runMachine(registers: dict[str, int], instructions: list[int]) -> list[int]:
  aRegister = registers['A']
  bRegister = registers['B']
  cRegister = registers['C']

  def getLiteralOperand(value: int) -> int:
    return value

  def getComboOperand(value: int) -> int:
    match value:
      case num if 0 <= num <= 3:
        return num
      case 4:
        return aRegister
      case 5:
        return bRegister
      case 6:
        return cRegister
      case 7:
        print('ERROR!')
        exit()
    print("Unexpected Operand value", value)
    exit()

  ip = 0
  output : list[int] = []
  while ip < len(instructions):
    operand = instructions[ip + 1]
    match instructions[ip]:
      case 0: # adv
        aRegister = aRegister // pow(2, getComboOperand(operand))
      case 1: # bxl
        bRegister = bRegister ^ getLiteralOperand(operand)
      case 2: # bst
        bRegister = getComboOperand(operand) % 8
      case 3: # jnz
        if aRegister != 0:
          ip = getLiteralOperand(operand) - 2 # subtract 2 so that the increment at end works
      case 4: # bxc
        bRegister = bRegister ^ cRegister
      case 5: # out
        output.append(getComboOperand(operand) % 8)
      case 6: # bdv
        bRegister = aRegister // pow(2, getComboOperand(operand))
      case 7: # cdv
        cRegister = aRegister // pow(2, getComboOperand(operand))
    ip += 2

  return output

registers, instructions = buildInitialState(data)
output = runMachine(registers, instructions)
print("Part 1 solution is ", ",".join(map(str, output)))


def findCopyValue(instructions: list[int]) -> int:
  aRegister = 0
  bRegister = 0
  cRegister = 0

  def getLiteralOperand(value: int) -> int:
    return value

  def getComboOperand(value: int) -> int:
    match value:
      case num if 0 <= num <= 3:
        return num
      case 4:
        return aRegister
      case 5:
        return bRegister
      case 6:
        return cRegister
      case 7:
        print('ERROR!')
        exit()
    print("Unexpected Operand value", value)
    exit()

  a = 0
  while True:
    if a % 1000000 == 0:
      print("... on iteration ", a)
    aRegister = a
    bRegister = 0
    cRegister = 0
    ip = 0
    outputIndex = 0
    while ip < len(instructions):
      operand = instructions[ip + 1]
      match instructions[ip]:
        case 0: # adv
          aRegister = aRegister // pow(2, getComboOperand(operand))
        case 1: # bxl
          bRegister = bRegister ^ getLiteralOperand(operand)
        case 2: # bst
          bRegister = getComboOperand(operand) % 8
        case 3: # jnz
          if aRegister != 0:
            ip = getLiteralOperand(operand) - 2 # subtract 2 so that the increment at end works
        case 4: # bxc
          bRegister = bRegister ^ cRegister
        case 5: # out
          output = getComboOperand(operand) % 8
          if outputIndex >= len(instructions) or instructions[outputIndex] != output:
            break
          outputIndex += 1
        case 6: # bdv
          bRegister = aRegister // pow(2, getComboOperand(operand))
        case 7: # cdv
          cRegister = aRegister // pow(2, getComboOperand(operand))
      ip += 2
    if outputIndex == len(instructions) and ip == len(instructions):
      return a
    a += 1


# print("Part 2 solution is ", findCopyValue(instructions))