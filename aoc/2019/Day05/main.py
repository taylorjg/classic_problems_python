from functools import partial
from enum import Enum


class Opcodes(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    OUTPUT = 4
    HALT = 99


def decode_instruction(instruction):
    instruction_string = str(instruction)
    opcode = Opcodes(int(instruction_string[-2:]))
    modes_string = instruction_string[:-2]
    left_padded_modes_string = modes_string.rjust(2, '0')
    reversed_modes_string = left_padded_modes_string[::-1]
    modes = [int(c) for c in reversed_modes_string]
    return opcode, modes


def execute_arithmetic_instruction(op, program, pos, modes):
    param1 = program[pos + 1]
    param2 = program[pos + 2]
    param3 = program[pos + 3]
    a = param1 if modes[0] else program[param1]
    b = param2 if modes[1] else program[param2]
    c = op(a, b)
    program[param3] = c
    return pos + 4


def execute_save_instruction(input, program, pos, _):
    param1 = program[pos + 1]
    program[param1] = input
    return pos + 2


def execute_output_instruction(outputs, program, pos, modes):
    param1 = program[pos + 1]
    output = param1 if modes[0] else program[param1]
    outputs.append(output)
    return pos + 2


def make_intcode_dict(input, outputs):
    return {
        Opcodes.ADD: partial(execute_arithmetic_instruction, lambda x, y: x + y),
        Opcodes.MULTIPLY: partial(execute_arithmetic_instruction, lambda x, y: x * y),
        Opcodes.SAVE: partial(execute_save_instruction, input),
        Opcodes.OUTPUT: partial(execute_output_instruction, outputs)
    }


def run_program(program, input):
    outputs = []
    intcode_dict = make_intcode_dict(input, outputs)
    pos = 0
    while True:
        instruction = program[pos]
        opcode, modes = decode_instruction(instruction)
        if opcode == Opcodes.HALT:
            break
        fn = intcode_dict[opcode]
        pos = fn(program, pos, modes)
    return outputs


def part1(program):
    outputs = run_program(program, 1)
    print(outputs)
    answer = outputs[-1]
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day05/input.txt") as f:
        line = f.read()
        program = [int(s) for s in line.split(',')]
        part1(program)
