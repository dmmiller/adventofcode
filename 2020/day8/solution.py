from __future__ import annotations
import re
import typing
from collections.abc import Iterable, Callable, Generator

#Type Information
Instruction = tuple[str, int]

instruction_re = re.compile(r"(?P<instruction>\w{3}) (?P<value>[+-]\d+)")

class Machine:

    def _acc(self, value : int) -> int:
        self.acc += value
        return 1

    INSTRUCTION_TABLE : dict[str, Callable[[Machine,int], int]] = {
        'acc' : _acc,
        'jmp' : lambda self, x: x,
        'nop' : lambda self, x: 1,
    }

    def __init__(self, instructions : Iterable[Instruction]):
        self.instructions = list(instructions)
        self.reset()

    def execute(self) -> Generator[int, None, None]:
        self.reset()
        while self.ip < len(self.instructions):
            yield self.ip
            self.ip += self._execute_instruction(self.ip)

    def _execute_instruction(self, ip : int) -> int:
        operation, value = self.instructions[ip]
        func = self.INSTRUCTION_TABLE[operation]
        return func(self, value)

    def reset(self) -> None:
        self.ip = 0
        self.acc = 0

    def execute_without_looping(self) -> bool:
        executed_instructions = set()
        for ip in self.execute():
            if ip in executed_instructions:
                return False
            executed_instructions.add(ip)
        return True

    def find_accumulator_before_loop(self) -> int:
        if not self.execute_without_looping():
            return self.acc
        return None

    def repair(self) -> int:
        for i in range(len(self.instructions)):
            old_operation, value = self.instructions[i]
            if old_operation == "jmp":
                new_operation = "nop"
            elif old_operation == "nop":
                new_operation = "jmp"
            else:
                continue
            self.instructions[i] = (new_operation, value)
            if self.execute_without_looping():
                print(f"Changed instruction {i} from ({old_operation} {value}) to ({new_operation} {value})")
                return self.acc
            self.instructions[i] = (old_operation, value)
        return None

    @staticmethod
    def parse_instruction(line : str) -> Instruction:
        match = instruction_re.match(line)
        return (match['instruction'], int(match['value']))


with open('input.txt') as f:
    machine = Machine(Machine.parse_instruction(line.strip()) for line in f)
    print(f"Accumulator value when loop detected is {machine.find_accumulator_before_loop()}")
    print(f"Accumulator value when machine is repaired {machine.repair()}")