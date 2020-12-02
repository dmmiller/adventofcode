from machine import Machine
from typing import List

class Amplifier:

    def __init__(self, instructions : List[int]):
        self.machine = Machine()
        self.machine.load(instructions)
        self.phase = 0
        self.input = 0

    def set_phase(self, phase : int) -> None:
        self.phase = phase
    
    def set_input(self, input : int) -> None:
        self.input = input

    def run(self) -> None:
        self.machine.run()
        assert(self.machine.awaiting_input())
        self.machine.set_input(self.phase)
        self.machine.run()
        assert(self.machine.awaiting_input())
        self.machine.set_input(self.input)
        self.machine.run()
        assert(self.machine.done())

    def get_output(self) -> int:
        return self.machine.get_output()

