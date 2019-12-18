from functools import partial
from enum import Enum
from collections import defaultdict
from itertools import groupby, chain


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


def find_start(grid):
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in "^v<>":
                return x, y
    return None


def move(direction, pos):
    x, y = pos
    if direction == "U": return x, y - 1
    if direction == "D": return x, y + 1
    if direction == "L": return x - 1, y
    if direction == "R": return x + 1, y
    raise ValueError(f"Unknown direction {direction}")


def opposite_direction(direction):
    if direction == "U": return "D"
    if direction == "D": return "U"
    if direction == "L": return "R"
    if direction == "R": return "L"
    raise ValueError(f"Unknown direction {direction}")


def within_grid(grid, pos):
    rows = len(grid)
    cols = len(grid[0])
    x, y = pos
    return 0 <= x < cols and 0 <= y < rows


def valid_pos(grid, pos):
    if not within_grid(grid, pos):
        return False
    x, y = pos
    if grid[y][x] == ".":
        return False
    return True


def try_follow_direction(grid, direction, pos):
    new_pos = move(direction, pos)
    return (direction, new_pos) if valid_pos(grid, new_pos) else None


def try_find_new_direction(grid, direction, pos):
    ds = [d for d in "UDLR"]
    if direction is not None:
        od = opposite_direction(direction)
        ds = [d for d in ds if d != od]
    v1 = [(d, move(d, pos)) for d in ds]
    v2 = [(d, p) for (d, p) in v1 if valid_pos(grid, p)]
    if len(v2) == 1:
        return v2[0]
    if len(v2) == 0:
        return None
    raise AssertionError("Expected 0 or 1 valid directions")


def follow_path(grid, start):
    current_dir = None
    current_pos = start
    pos_dict = defaultdict(int)
    directions = []
    while True:
        next_dir_pos = None
        if current_dir is not None:
            next_dir_pos = try_follow_direction(grid, current_dir, current_pos)
        if next_dir_pos is None:
            next_dir_pos = try_find_new_direction(grid, current_dir, current_pos)
        if next_dir_pos is None:
            break
        current_dir, current_pos = next_dir_pos
        directions.append(current_dir)
        pos_dict[current_pos] += 1
    print("".join(directions))
    v1 = groupby(directions)
    v2 = [(k, len(list(v))) for k, v in v1]
    for v3 in v2:
        print(v3)
    return pos_dict


def part1(values):
    program = Program(values)
    outputs = run_program(program, [])
    s = "".join([chr(code) for code in outputs])
    rows = s.split('\n')
    grid = [row for row in rows if len(row) > 0]
    for row in grid: print(row)
    start = find_start(grid)
    pos_dict = follow_path(grid, start)
    intersections = [pos for pos, count in pos_dict.items() if count > 1]
    answer = sum([x * y for (x, y) in intersections])
    print(f"part 1 answer: {answer}")


def make_inputs():
    fn_main = "A,B,C,B,A,C"
    fn_a = "R,8,R,8"
    fn_b = "R,4,R,4,R,8"
    fn_c = "L,6,L,2"
    yes_no = "n"
    s = "\n".join([fn_main, fn_a, fn_b, fn_c, yes_no]) + "\n"
    return [ord(ch) for ch in s]


def part2(values):
    values[0] = 2
    program = Program(values)
    inputs = make_inputs()
    outputs = run_program(program, inputs)
    s = "".join([chr(code) for code in outputs])
    rows = s.split('\n')
    grid = [row for row in rows if len(row) > 0]
    for row in grid: print(row)
    print(f"part 2 answer: {0}")


if __name__ == "__main__":
    with open("aoc/2019/Day17/input.txt") as f:
        line = f.read()
        values = [int(s) for s in line.split(',')]
        # part1(values)
        part2(values)
