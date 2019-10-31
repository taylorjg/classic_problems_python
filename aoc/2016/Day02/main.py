part_1_keypad = [
    "123",
    "456",
    "789"
]

part_2_keypad = [
    "  1  ",
    " 234 ",
    "56789",
    " ABC ",
    "  D  "
]

keypads = {
    1: part_1_keypad,
    2: part_2_keypad
}


def move(keypad, pos, direction):
    last_row = len(keypad) - 1
    last_col = len(keypad[0]) - 1

    def try_move(new_row, new_col):
        if new_row < 0 or new_col < 0: return pos
        if new_row > last_row or new_col > last_col: return pos
        if keypad[new_row][new_col] == " ": return pos
        return new_row, new_col

    row, col = pos

    if direction == "U": return try_move(row - 1, col)
    if direction == "D": return try_move(row + 1, col)
    if direction == "L": return try_move(row, col - 1)
    if direction == "R": return try_move(row, col + 1)
    raise ValueError(f"Unknown direction, {direction}.")


def find_start_pos(keypad):
    rows = range(len(keypad))
    cols = range(len(keypad[0]))
    for row in rows:
        for col in cols:
            if keypad[row][col] == '5':
                return row, col
    raise ValueError(f"Failed to find '5' in keypad.")


def calc_bathroom_code(part, instructions):
    keypad = keypads[part]
    start_pos = find_start_pos(keypad)
    current_pos = start_pos
    code = []
    for instruction in instructions:
        for direction in instruction:
            current_pos = move(keypad, current_pos, direction)
        row, col = current_pos
        code.append(keypad[row][col])
    print(f"part {part} answer: {''.join(code)}")


if __name__ == "__main__":
    with open("aoc/2016/Day02/input.txt") as f:
        instructions = [line.rstrip() for line in f.readlines()]
        calc_bathroom_code(1, instructions)
        calc_bathroom_code(2, instructions)
