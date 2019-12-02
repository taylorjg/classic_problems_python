def run_program(program, noun, verb):
    program = program.copy()
    program[1] = noun
    program[2] = verb
    pos = 0
    while True:
        opcode = program[pos]
        if opcode == 99:
            break
        a = program[program[pos + 1]]
        b = program[program[pos + 2]]
        c = a + b if opcode == 1 else a * b
        program[program[pos + 3]] = c
        pos = pos + 4
    return program[0]


def part1(program):
    output = run_program(program, 12, 2)
    print(f"part 1 answer: {output}")


def find_noun_verb(program):
    for noun in range(0, 100):
        for verb in range(0, 100):
            output = run_program(program, noun, verb)
            if output == 19690720:
                return noun, verb
    return None


def part2(program):
    noun, verb = find_noun_verb(program)
    print(f"part 2 answer: {noun * 100 + verb}")


if __name__ == "__main__":
    with open("aoc/2019/Day02/input.txt") as f:
        line = f.read()
        program = [int(s) for s in line.split(',')]
        part1(program)
        part2(program)
