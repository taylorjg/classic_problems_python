from functools import partial
from enum import Enum
from collections import defaultdict
import math


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


def execute_save_instruction(inputs, program, modes):
    program.set_param(modes, 1, inputs.pop(0))
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


def make_intcode_dict(inputs, outputs):
    return {
        Opcodes.ADD: partial(execute_arithmetic_instruction, lambda a, b: a + b),
        Opcodes.MULTIPLY: partial(execute_arithmetic_instruction, lambda a, b: a * b),
        Opcodes.SAVE: partial(execute_save_instruction, inputs),
        Opcodes.OUTPUT: partial(execute_output_instruction, outputs),
        Opcodes.JUMP_IF_TRUE: partial(execute_jump_instruction, lambda a: a),
        Opcodes.JUMP_IF_FALSE: partial(execute_jump_instruction, lambda a: not a),
        Opcodes.LESS_THAN: partial(execute_comparison_instruction, lambda a, b: a < b),
        Opcodes.EQUALS: partial(execute_comparison_instruction, lambda a, b: a == b),
        Opcodes.ADJUST_REL: execute_adjust_rel_instruction
    }


def run_program(program, inputs):
    outputs = []
    intcode_dict = make_intcode_dict(inputs, outputs)
    while True:
        instruction = program.get_current_instruction()
        opcode, modes = decode_instruction(instruction)
        if opcode == Opcodes.HALT:
            break
        fn = intcode_dict[opcode]
        program.pos = fn(program, modes)
    return outputs


def split_list_every(xs, n):
    num_layers = len(xs) // n
    for idx in range(num_layers):
        start_idx = idx * n
        end_idx = start_idx + n
        yield xs[start_idx:end_idx]


def part1(values):
    outputs = []
    start_row = 1000
    end_row = 1010
    width = end_row
    row_range = range(start_row, end_row)
    for y in row_range:
        for x in range(width):
            program = Program(values)
            outputs += run_program(program, [x, y])

    chars = [("#" if output == 1 else ".") for output in outputs]
    rows = list(split_list_every(chars, width))
    for row in rows:
        print("".join(row))

    # print()
    # last_row = "".join(rows[-1])
    # x1 = last_row.find("#")
    # x2 = last_row.rfind("#")
    # print(f"x1: {x1}; x2: {x2}")
    # a1 = math.atan(x1 / end_row)
    # a2 = math.atan(x2 / end_row)
    # print(f"a1: {a1} ({math.degrees(a1)}); a2: {a2} ({math.degrees(a2)})")
    # print()

    # a1: 0.5404195002705842 (30.96375653207352);
    # a2: 0.6107259643892086 (34.99202019855866)
    # a1 = 0.5404195002705842
    # a2 = 0.6107259643892086

    # a1 = 0.583373006993856  # (33.424811182603804)
    # a2 = 0.6747409422235527  # (38.659808254090095)

    # calculated from the 1000th row:
    # a1 = 0.583373006993856  # (33.424811182603804)
    # a2 = 0.6957210768630759  # (39.861881422551)
    a1 = 0.583373006993856  # (33.424811182603804)
    a2 = 0.6957210768630759  # (39.861881422551)
    # a1 = math.radians(33.4)
    # a2 = math.radians(39.8)

    print()

    for y in row_range:
        if y == 0:
            # idx1 = 0
            # idx2 = 1
            v1 = 0
            v2 = 0
        else:
            # idx1 = my_round_1((y + 1) * math.tan(a1))
            # idx2 = my_round_2((y + 1) * math.tan(a2))
            v1 = (y + 1) * math.tan(a1)
            v2 = (y + 1) * math.tan(a2)
            # idx1 = int(v1)
            # idx2 = idx1 + round(v2 - v1)
        s = None
        e = None
        row = "".join(rows[y - start_row])
        if "#" in row:
            s = row.find("#")
            e = row.rfind("#")
        diff = round(v2 - v1, 2)
        mid = round((v1 + v2) / 2, 2)
        if y != 0 and diff < 0.4:
            v1 = None
            v2 = None
        else:
            v1 = round(v1)
            v2 = round(v2)
        print(f"y: {y}; s: {s}; e: {e}; v1: {v1}; v2: {v2}; diff: {diff}; mid: {mid}")
        # row2 = ("." * idx1) + ("#" * (idx2 - idx1 + 1)) + ("." * (size - idx2 - 1))
        # row2 = ("." * idx1) + ("#" * (idx2 - idx1)) + ("." * (size - idx2 - 1))
        # print(row2)

    answer = outputs.count(1)
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day19/input.txt") as f:
        line = f.read()
        values = [int(s) for s in line.split(',')]
        part1(values)
