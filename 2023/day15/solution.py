
data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""

with open("input.txt") as f:
  data = f.read()


def hash(s: str) -> int:
  currentValue = 0
  for i in range(len(s)):
    currentValue += ord(s[i])
    currentValue *= 17
    currentValue %= 256
  return currentValue


def hashMap(sequence: str) -> int:
  boxes: list[list[(str, int)]] = [[] for i in range(256)]
  labels: set[str] = set()
  for step in sequence.split(","):
    dash = step.find("-")
    if dash != -1:
      label = step[:dash]
      boxNumber = hash(label)
      if label in labels:
        slot = 0
        for i, pair in enumerate(boxes[boxNumber]):
          if pair[0] == label:
            slot = i
            break
        boxes[boxNumber] = boxes[boxNumber][:slot] + \
            boxes[boxNumber][slot + 1:]
        labels.remove(label)
    else:
      equal = step.find("=")
      label = step[:equal]
      boxNumber = hash(label)
      lens = int(step[equal + 1])
      if label in labels:
        slot = 0
        for i, pair in enumerate(boxes[boxNumber]):
          if pair[0] == label:
            slot = i
            break
        boxes[boxNumber][slot] = (label, lens)
      else:
        boxes[boxNumber].append((label, lens))
        labels.add(label)

  total = 0
  for i, box in enumerate(boxes):
    for j, p in enumerate(box):
      total += ((i + 1) * (j + 1) * p[1])

  return total


print("Part 1 solution : ", sum(hash(s) for s in data.split(",")))
print("Part 2 solution : ", hashMap(data))
