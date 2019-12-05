def run_program(program, input):
    outputs = []
    pos = 0
    while True:
        instruction = str(program[pos])
        opcode = int(instruction[-2:])
        raw_modes = instruction[:-2]
        padded_raw_modes = raw_modes.rjust(3, '0')
        [modea, modeb, _] = [int(c) for c in padded_raw_modes[::-1]]
        if opcode == 99:  # halt
            break
        if opcode == 1:  # add
            param1 = program[pos + 1]
            param2 = program[pos + 2]
            param3 = program[pos + 3]
            a = param1 if modea else program[param1]
            b = param2 if modeb else program[param2]
            program[param3] = a + b
            pos = pos + 4
        if opcode == 2:  # multiply
            param1 = program[pos + 1]
            param2 = program[pos + 2]
            param3 = program[pos + 3]
            a = param1 if modea else program[param1]
            b = param2 if modeb else program[param2]
            program[param3] = a * b
            pos = pos + 4
        if opcode == 3:  # save
            param1 = program[pos + 1]
            program[param1] = input
            pos = pos + 2
        if opcode == 4:  # output
            param1 = program[pos + 1]
            output = param1 if modea else program[param1]
            outputs.append(output)
            print(output)
            pos = pos + 2
    return outputs


def part1(program):
    output = run_program(program, 1)
    print(f"part 1 answer: {output}")


if __name__ == "__main__":
    with open("aoc/2019/Day05/input.txt") as f:
        line = f.read()
        program = [int(s) for s in line.split(',')]
        part1(program)
