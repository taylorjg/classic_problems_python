from functools import partial
from enum import Enum
from collections import defaultdict


class Opcodes(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_REL = 9
    HALT = 99


class Modes(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Program:
    def __init__(self, values):
        self.program = defaultdict(int)
        for addr, value in enumerate(values):
            self.program[addr] = value
        self.pos = 0
        self.rel = 0

    def get_current_instruction(self):
        return self.program[self.pos]

    def get_param(self, modes, param_num):
        mode = modes[param_num - 1]
        addr = self.program[self.pos + param_num]
        if mode == Modes.IMMEDIATE:
            return addr
        if mode == Modes.POSITION:
            return self.program[addr]
        if mode == Modes.RELATIVE:
            return self.program[self.rel + addr]
        raise ValueError(f"Unknown mode: {mode}.")

    def set_param(self, modes, param_num, value):
        mode = modes[param_num - 1]
        addr = self.program[self.pos + param_num]
        if mode == Modes.IMMEDIATE:
            raise ValueError(f"Mode not supported for set_param: {mode}.")
        if mode == Modes.POSITION:
            self.program[addr] = value
            return
        if mode == Modes.RELATIVE:
            self.program[self.rel + addr] = value
            return
        raise ValueError(f"Unknown mode: {mode}.")


def decode_instruction(instruction):
    instruction_string = str(instruction)
    opcode = Opcodes(int(instruction_string[-2:]))
    modes_string = instruction_string[:-2]
    left_padded_modes_string = modes_string.rjust(3, '0')
    reversed_modes_string = left_padded_modes_string[::-1]
    modes = [Modes(int(c)) for c in reversed_modes_string]
    return opcode, modes


def execute_arithmetic_instruction(op, program, modes):
    a = program.get_param(modes, 1)
    b = program.get_param(modes, 2)
    c = op(a, b)
    program.set_param(modes, 3, c)
    return program.pos + 4


def execute_save_instruction(input, program, modes):
    program.set_param(modes, 1, input)
    return program.pos + 2


def execute_output_instruction(outputs, program, modes):
    output = program.get_param(modes, 1)
    outputs.append(output)
    return program.pos + 2


def execute_jump_instruction(op, program, modes):
    a = program.get_param(modes, 1)
    b = program.get_param(modes, 2)
    return b if op(a) else program.pos + 3


def execute_comparison_instruction(op, program, modes):
    a = program.get_param(modes, 1)
    b = program.get_param(modes, 2)
    c = op(a, b)
    program.set_param(modes, 3, c)
    return program.pos + 4


def execute_adjust_rel_instruction(program, modes):
    offset = program.get_param(modes, 1)
    program.rel = program.rel + offset
    return program.pos + 2


def make_intcode_dict(input, outputs):
    return {
        Opcodes.ADD: partial(execute_arithmetic_instruction, lambda a, b: a + b),
        Opcodes.MULTIPLY: partial(execute_arithmetic_instruction, lambda a, b: a * b),
        Opcodes.SAVE: partial(execute_save_instruction, input),
        Opcodes.OUTPUT: partial(execute_output_instruction, outputs),
        Opcodes.JUMP_IF_TRUE: partial(execute_jump_instruction, lambda a: a),
        Opcodes.JUMP_IF_FALSE: partial(execute_jump_instruction, lambda a: not a),
        Opcodes.LESS_THAN: partial(execute_comparison_instruction, lambda a, b: a < b),
        Opcodes.EQUALS: partial(execute_comparison_instruction, lambda a, b: a == b),
        Opcodes.ADJUST_REL: execute_adjust_rel_instruction
    }


def run_program(program, input):
    outputs = []
    intcode_dict = make_intcode_dict(input, outputs)
    while True:
        instruction = program.get_current_instruction()
        opcode, modes = decode_instruction(instruction)
        if opcode == Opcodes.HALT:
            break
        fn = intcode_dict[opcode]
        program.pos = fn(program, modes)
    return outputs


def part1(values):
    program = Program(values)
    outputs = run_program(program, 1)
    print(f"part 1 answer: {outputs[0]}")


def part2(values):
    program = Program(values)
    outputs = run_program(program, 2)
    print(f"part 2 answer: {outputs[0]}")


if __name__ == "__main__":
    with open("aoc/2019/Day09/input.txt") as f:
        line = f.read()
        values = [int(s) for s in line.split(',')]
        part1(values)
        part2(values)
