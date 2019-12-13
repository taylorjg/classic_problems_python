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


def run_program_until_next_instruction(program, input):
    outputs = []
    intcode_dict = make_intcode_dict(input, outputs)
    while True:
        instruction = program.get_current_instruction()
        opcode, modes = decode_instruction(instruction)
        if opcode == Opcodes.HALT:
            return None
        fn = intcode_dict[opcode]
        program.pos = fn(program, modes)
        if len(outputs) == 3:
            return outputs


def split_list_every(xs, n):
    num_layers = len(xs) // n
    for idx in range(num_layers):
        start_idx = idx * n
        end_idx = start_idx + n
        yield xs[start_idx:end_idx]


SCREEN_WIDTH = 40
SCREEN_HEIGHT = 24

EMPTY_TILE_ID = 0
WALL_TILE_ID = 1
BLOCK_TILE_ID = 2
PADDLE_TILE_ID = 3
BALL_TILE_ID = 4

EMPTY_CHAR = " "
WALL_CHAR = "#"
BLOCK_CHAR = "."
PADDLE_CHAR = "-"
BALL_CHAR = "o"

SCREEN_CHARS = {
    EMPTY_TILE_ID: EMPTY_CHAR,
    WALL_TILE_ID: WALL_CHAR,
    BLOCK_TILE_ID: BLOCK_CHAR,
    PADDLE_TILE_ID: PADDLE_CHAR,
    BALL_TILE_ID: BALL_CHAR
}


def read_initial_screen(program):
    screen = {}
    for _ in range(SCREEN_WIDTH * SCREEN_HEIGHT):
        [x, y, tile_id] = run_program_until_next_instruction(program, 0)
        screen[x, y] = SCREEN_CHARS[tile_id]
    return screen


def draw_screen(screen):
    for y in range(SCREEN_HEIGHT):
        row = [screen[x, y] for x in range(SCREEN_WIDTH)]
        print("".join(row))
    print()


def calc_joystick_tilt(ball_pos_x, paddle_pos_x):
    if ball_pos_x > paddle_pos_x: return +1
    if ball_pos_x < paddle_pos_x: return -1
    return 0


def part1(values):
    program = Program(values)
    outputs = run_program(program, 0)
    instructions = list(split_list_every(outputs, 3))
    tile_ids = [tile_id for [_, _, tile_id] in instructions]
    answer = tile_ids.count(2)
    print(f"part 1 answer: {answer}")


def part2(values):
    values[0] = 2
    program = Program(values)
    screen = read_initial_screen(program)
    # draw_screen(screen)
    ball_pos_x = 0
    paddle_pos_x = 0
    current_score = 0
    joystick_tilt = 0
    while True:
        instruction = run_program_until_next_instruction(program, joystick_tilt)
        if instruction is None: break
        [x, y, tile_id] = instruction
        if x == -1 and y == 0:
            current_score = tile_id
            continue
        screen[x, y] = SCREEN_CHARS[tile_id]
        if tile_id == EMPTY_TILE_ID: continue
        if tile_id == BALL_TILE_ID: ball_pos_x = x
        if tile_id == PADDLE_TILE_ID: paddle_pos_x = x
        # draw_screen(screen)
        joystick_tilt = calc_joystick_tilt(ball_pos_x, paddle_pos_x)
    # draw_screen(screen)
    print(f"part 2 answer: {current_score}")


if __name__ == "__main__":
    with open("aoc/2019/Day13/input.txt") as f:
        line = f.read()
        values = [int(s) for s in line.split(',')]
        part1(values)
        part2(values)
