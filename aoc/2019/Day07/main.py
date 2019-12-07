from functools import partial
from itertools import permutations
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


def execute_save_instruction(inputs, program, pos, _):
    next_input = inputs.pop(0)
    param1 = program[pos + 1]
    program[param1] = next_input
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


def make_intcode_dict(inputs, outputs):
    return {
        Opcodes.ADD: partial(execute_arithmetic_instruction, lambda a, b: a + b),
        Opcodes.MULTIPLY: partial(execute_arithmetic_instruction, lambda a, b: a * b),
        Opcodes.SAVE: partial(execute_save_instruction, inputs),
        Opcodes.OUTPUT: partial(execute_output_instruction, outputs),
        Opcodes.JUMP_IF_TRUE: partial(execute_jump_instruction, lambda a: a),
        Opcodes.JUMP_IF_FALSE: partial(execute_jump_instruction, lambda a: not a),
        Opcodes.LESS_THAN: partial(execute_comparison_instruction, lambda a, b: a < b),
        Opcodes.EQUALS: partial(execute_comparison_instruction, lambda a, b: a == b)
    }


def run_program(program, inputs):
    outputs = []
    intcode_dict = make_intcode_dict(inputs, outputs)
    pos = 0
    while True:
        instruction = program[pos]
        opcode, modes = decode_instruction(instruction)
        if opcode == Opcodes.HALT:
            break
        fn = intcode_dict[opcode]
        pos = fn(program, pos, modes)
    return outputs


def run_amplifier(program, setting, input):
    program = program.copy()
    outputs = run_program(program, [setting, input])
    return outputs[0]


def try_phase_settings(program, settings):
    a = run_amplifier(program, settings[0], 0)
    b = run_amplifier(program, settings[1], a)
    c = run_amplifier(program, settings[2], b)
    d = run_amplifier(program, settings[3], c)
    e = run_amplifier(program, settings[4], d)
    return e


def find_best_thruster_signal(program):
    perms = permutations(range(5), 5)
    outputs = [try_phase_settings(program, perm) for perm in perms]
    return sorted(outputs, reverse=True)[0]


def make_program(program_source):
    return [int(s) for s in program_source.split(',')]


def part1_tests():
    def part1_test(program_source):
        program = make_program(program_source)
        print(f"best thruster signal: {find_best_thruster_signal(program)}")

    program_source_1 = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
    program_source_2 = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    program_source_3 = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    part1_test(program_source_1)
    part1_test(program_source_2)
    part1_test(program_source_3)


def part1(program):
    answer = find_best_thruster_signal(program)
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
    part1_tests()
    with open("aoc/2019/Day07/input.txt") as f:
        program = make_program(f.read())
        part1(program)
