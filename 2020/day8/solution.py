import re

instruction_re = re.compile(r"(?P<instruction>\w{3}) (?P<value>[+-]\d+)")

class Machine:

    def _acc(self, value):
        self.acc += value
        return 1

    INSTRUCTION_TABLE = {
        'acc' : _acc,
        'jmp' : lambda self, x: x,
        'nop' : lambda self, x: 1,
    }

    def __init__(self, instructions):
        self.instructions = list(instructions)
        self.reset()

    def execute(self):
        self.reset()
        executed_instructions = set()
        while self.ip not in executed_instructions:
            executed_instructions.add(self.ip)
            if self.ip >= len(self.instructions):
                return True
            self.ip += self.execute_instruction(self.ip)
        return False

    def execute_instruction(self, ip):
        operation, value = self.instructions[ip]
        func = self.INSTRUCTION_TABLE[operation]
        return func(self, value)

    def reset(self):
        self.ip = 0
        self.acc = 0

    def find_accumulator_before_loop(self):
        if not self.execute():
            return self.acc
        return None
    
    def repair(self):
        for i in range(len(self.instructions)):
            old_operation, value = self.instructions[i]
            if old_operation == "acc":
                continue
            if old_operation == "nop":
                new_operation = "jmp"
            else:
                new_operation = "nop"
            self.instructions[i] = (new_operation, value)
            if self.execute():
                print(f"Changed instruction {i} from ({old_operation} {value}) to ({new_operation} {value})")
                return self.acc
            self.instructions[i] = (old_operation, value)
        return None

    @classmethod
    def parse_instruction(cls, line):
        match = instruction_re.match(line)
        return (match.group('instruction'), int(match.group('value')))


with open('input.txt') as f:
    instructions = [Machine.parse_instruction(line.strip()) for line in f]
    machine = Machine(instructions)
    print(f"Accumulator value when loop detected is {machine.find_accumulator_before_loop()}")
    print(f"Accumulator value when machine is repaired {machine.repair()}")