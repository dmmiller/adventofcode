from dataclasses import dataclass, field
from math import prod

data = """C0015000016115A2E0802F182340"""

with open("input.txt") as f:
    data = f.read()


@dataclass
class LiteralPacket:
    version: int
    type: int
    value: int


@dataclass
class OperatorPacket:
    version: int
    type: int
    packets: list = field(default_factory=list)


def toBinary(data: str) -> str:
    return "".join(format(int(c, base=16), "0=4b") for c in data)


def parsePacket(s: str):

    def parsePacketSub(offset):
        version = int(s[offset:offset + 3], base=2)
        offset += 3
        type = int(s[offset: offset + 3], base=2)
        offset += 3
        if type == 4:
            bits = ""
            lastGroupProcessed = False
            while not lastGroupProcessed:
                if s[offset] == "0":
                    lastGroupProcessed = True
                bits += s[offset + 1: offset + 5]
                offset += 5
            value = int(bits, base=2)
            return LiteralPacket(version, type, value), offset
        else:
            length_type_id = s[offset]
            offset += 1
            if length_type_id == "0":
                subpackets_length = int(s[offset: offset + 15], base=2)
                offset += 15
                new_offset = offset
                packets = []
                while new_offset - offset < subpackets_length:
                    packet, new_offset = parsePacketSub(new_offset)
                    packets.append(packet)
                assert new_offset == offset + subpackets_length
                return OperatorPacket(version, type, packets), new_offset
            else:
                number_packets = int(s[offset: offset + 11], base=2)
                offset += 11
                packets = []
                for i in range(number_packets):
                    packet, offset = parsePacketSub(offset)
                    packets.append(packet)
                return OperatorPacket(version, type, packets), offset
            return None, offset

    return parsePacketSub(0)[0]


def computeVersionSum(packet):
    if isinstance(packet, LiteralPacket):
        return packet.version
    elif isinstance(packet, OperatorPacket):
        return sum(computeVersionSum(p) for p in packet.packets) + packet.version


binary = toBinary(data)
packet = parsePacket(binary)
print(f"Part 1 : Sum of packet versions is {computeVersionSum(packet)}")


def evaluatePacket(packet):
    if isinstance(packet, LiteralPacket):
        return packet.value
    elif isinstance(packet, OperatorPacket):
        match packet.type:
            case 0:
                return sum(evaluatePacket(p) for p in packet.packets)
            case 1:
                return prod(evaluatePacket(p) for p in packet.packets)
            case 2:
                return min(evaluatePacket(p) for p in packet.packets)
            case 3:
                return max(evaluatePacket(p) for p in packet.packets)
            case 5:
                first = evaluatePacket(packet.packets[0])
                second = evaluatePacket(packet.packets[1])
                return 1 if first > second else 0
            case 6:
                first = evaluatePacket(packet.packets[0])
                second = evaluatePacket(packet.packets[1])
                return 1 if first < second else 0
            case 7:
                first = evaluatePacket(packet.packets[0])
                second = evaluatePacket(packet.packets[1])
                return 1 if first == second else 0
            case _:
                assert "Unknown packet typ"
    assert "Unknown object"


print(
    f"Part 2 : Evaluating the packet expression yield {evaluatePacket(packet)}")
