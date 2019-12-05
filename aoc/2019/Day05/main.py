from functools import partial
from enum import Enum


class Opcodes(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


def decode_instruction(instruction):
    instruction_string = str(instruction)
    opcode = Opcodes(int(instruction_string[-2:]))
    modes_string = instruction_string[:-2]
    left_padded_modes_string = modes_string.rjust(2, '0')
    reversed_modes_string = left_padded_modes_string[::-1]
    modes = [int(c) for c in reversed_modes_string]
    return opcode, modes


def get_param(program, pos, modes, param_num):
    value = program[pos + param_num]
    return value if modes[param_num - 1] else program[value]


def execute_arithmetic_instruction(op, program, pos, modes):
    a = get_param(program, pos, modes, 1)
    b = get_param(program, pos, modes, 2)
    c = op(a, b)
    param3 = program[pos + 3]
    program[param3] = c
    return pos + 4


def execute_save_instruction(input, program, pos, _):
    param1 = program[pos + 1]
    program[param1] = input
    return pos + 2


def execute_output_instruction(outputs, program, pos, modes):
    output = get_param(program, pos, modes, 1)
    outputs.append(output)
    return pos + 2


def execute_jump_instruction(op, program, pos, modes):
    a = get_param(program, pos, modes, 1)
    b = get_param(program, pos, modes, 2)
    return b if op(a) else pos + 3


def execute_comparison_instruction(op, program, pos, modes):
    a = get_param(program, pos, modes, 1)
    b = get_param(program, pos, modes, 2)
    param3 = program[pos + 3]
    program[param3] = op(a, b)
    return pos + 4


def make_intcode_dict(input, outputs):
    return {
        Opcodes.ADD: partial(execute_arithmetic_instruction, lambda a, b: a + b),
        Opcodes.MULTIPLY: partial(execute_arithmetic_instruction, lambda a, b: a * b),
        Opcodes.SAVE: partial(execute_save_instruction, input),
        Opcodes.OUTPUT: partial(execute_output_instruction, outputs),
        Opcodes.JUMP_IF_TRUE: partial(execute_jump_instruction, lambda a: a),
        Opcodes.JUMP_IF_FALSE: partial(execute_jump_instruction, lambda a: not a),
        Opcodes.LESS_THAN: partial(execute_comparison_instruction, lambda a, b: a < b),
        Opcodes.EQUALS: partial(execute_comparison_instruction, lambda a, b: a == b)
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
    program = program.copy()
    outputs = run_program(program, 1)
    answer = outputs[-1]
    print(f"part 1 answer: {answer}")


def part2(program):
    program = program.copy()
    outputs = run_program(program, 5)
    answer = outputs[-1]
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day05/input.txt") as f:
        line = f.read()
        program = [int(s) for s in line.split(',')]
        part1(program)
        part2(program)
