from enum import IntEnum
from typing import List

class Machine:

    class ParameterMode(IntEnum):
        POSITION = 0
        IMMEDIATE = 1
    
    class Instruction(IntEnum):
        ADD = 1
        MULTIPLY = 2
        INPUT = 3
        OUTPUT = 4
        JUMP_IF_TRUE = 5
        JUMP_IF_FALSE = 6
        LESS_THAN = 7
        EQUALS = 8
        HALT = 99

    class State(IntEnum):
        READY = 0
        RUNNING = 1
        AWAITING_INPUT = 2
        DONE = 3
        ERROR = 4

    ip = 0
    memory = []
    io_value = None
    state = State.READY

    def load(self, memory : List[int]) -> None:
        self.memory = list(memory)

    def reset(self) -> None:
        self.ip = 0
        self.memory = []
        self.io_value = None
        self.state = self.State.READY

    def update(self, position : int, value : int):
        self.memory[position] = value

    def set_input(self, value: int) -> None:
        self.io_value = value

    def get_output(self) -> int:
        return self.io_value

    def get_memory_slot(self, idx : int) -> int:
        return self.memory[idx]
    
    def done(self) -> bool:
        return self.state == self.State.DONE
    
    def awaiting_input(self) -> bool:
        return self.state == self.State.AWAITING_INPUT

    def run(self) -> None:
        self.state = self.State.RUNNING
        running = True
        while running:
            op, modes = self.__parse_op_code(self.ip)
            if op == self.Instruction.ADD or op == self.Instruction.MULTIPLY:
                arg1 = self.__load_parameter(self.ip + 1, modes[0])
                arg2 = self.__load_parameter(self.ip + 2, modes[1])
                addr3 = self.memory[self.ip + 3]
                if op == self.Instruction.ADD:
                    self.memory[addr3] = arg1 + arg2
                elif op == self.Instruction.MULTIPLY:
                    self.memory[addr3] = arg1 * arg2                
                self.ip += 4
            elif op == self.Instruction.INPUT:
                if self.io_value == None:
#                    print ('Awaiting Input')
                    self.state = self.State.AWAITING_INPUT
                    running = False
                else:
#                    print ('Consuming Input ', self.io_value)
                    addr = self.memory[self.ip + 1]
                    self.memory[addr] = self.io_value
                    self.io_value = None
                    self.ip += 2
            elif op == self.Instruction.OUTPUT:
                arg = self.__load_parameter(self.ip + 1, modes[0])
                self.io_value = arg
#                print ('Output is ', arg)
                self.ip += 2
            elif op == self.Instruction.JUMP_IF_TRUE:
                arg = self.__load_parameter(self.ip + 1, modes[0])
                if arg != 0:
                    self.ip = self.__load_parameter(self.ip + 2, modes[1])
                else:
                    self.ip += 3
            elif op == self.Instruction.JUMP_IF_FALSE:
                arg = self.__load_parameter(self.ip + 1, modes[0])
                if arg == 0:
                    self.ip = self.__load_parameter(self.ip + 2, modes[1])
                else:
                    self.ip += 3
            elif op == self.Instruction.LESS_THAN:
                parameter1 = self.__load_parameter(self.ip + 1, modes[0])
                parameter2 = self.__load_parameter(self.ip + 2, modes[1])
                less_than = 0
                if parameter1 < parameter2:
                    less_than = 1
                addr = self.memory[self.ip + 3]
                self.memory[addr] = less_than
                self.ip += 4
            elif op == self.Instruction.EQUALS:
                parameter1 = self.__load_parameter(self.ip + 1, modes[0])
                parameter2 = self.__load_parameter(self.ip + 2, modes[1])
                equal = 0
                if parameter1 == parameter2:
                    equal = 1
                addr = self.memory[self.ip + 3]
                self.memory[addr] = equal
                self.ip += 4
            elif op == self.Instruction.HALT:
                self.state = self.State.DONE
                running = False
            else:
                print('Unrecognized Op Code ', op)
                running = False
                self.state = self.State.ERROR

    def dump(self) -> None:
        print (self.memory)

    def __parse_op_code(self, ip : int):
        op = self.memory[ip]
        instruction = op % 100
        mode_length = 2
        modes = []
        op = int (op / 100)
        while len(modes) < mode_length:
            if op % 2 == 0 :
                modes.append(0)
            else:
                modes.append(1)
            op = int(op / 10)

        return instruction, modes

    def __load_parameter(self, ip : int, mode: ParameterMode) -> int:
        parameter = self.memory[ip]
        if mode == self.ParameterMode.POSITION:
            return self.memory[parameter]
        elif mode == self.ParameterMode.IMMEDIATE:
            return parameter
        else:
            print ("We can't load the parameter")
            exit()

