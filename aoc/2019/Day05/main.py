ADD = 1
MULTIPLY = 2
SAVE = 3
OUTPUT = 4
HALT = 99


# TODO: add a dictionary of opcode to function to execute

def decode_instruction(instruction):
    instruction_string = str(instruction)
    opcode = int(instruction_string[-2:])
    modes_string = instruction_string[:-2]
    left_padded_modes_string = modes_string.rjust(2, '0')
    reversed_modes_string = left_padded_modes_string[::-1]
    modes = [int(c) for c in reversed_modes_string]
    return opcode, modes


def execute_arithmetic_instruction(program, pos, modes, op):
    param1 = program[pos + 1]
    param2 = program[pos + 2]
    param3 = program[pos + 3]
    a = param1 if modes[0] else program[param1]
    b = param2 if modes[1] else program[param2]
    c = op(a, b)
    program[param3] = c
    return pos + 4


def execute_save_instruction(program, pos, input):
    param1 = program[pos + 1]
    program[param1] = input
    return pos + 2


def execute_output_instruction(program, pos, modes, outputs):
    param1 = program[pos + 1]
    output = param1 if modes[0] else program[param1]
    outputs.append(output)
    return pos + 2


def run_program(program, input):
    outputs = []
    pos = 0
    while True:
        instruction = program[pos]
        opcode, modes = decode_instruction(instruction)
        if opcode == ADD:
            pos = execute_arithmetic_instruction(program, pos, modes, lambda x, y: x + y)
        if opcode == MULTIPLY:
            pos = execute_arithmetic_instruction(program, pos, modes, lambda x, y: x * y)
        if opcode == SAVE:
            pos = execute_save_instruction(program, pos, input)
        if opcode == OUTPUT:
            pos = execute_output_instruction(program, pos, modes, outputs)
        if opcode == HALT:
            break
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
