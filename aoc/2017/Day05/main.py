def part1(jumps):
    current_pos = 0
    steps = 0
    while 0 <= current_pos < len(jumps):
        offset = jumps[current_pos]
        new_pos = current_pos + offset
        jumps[current_pos] = offset + 1
        current_pos = new_pos
        steps = steps + 1
    print(f"part 1 answer: {steps}")


def part2(jumps):
    current_pos = 0
    steps = 0
    while 0 <= current_pos < len(jumps):
        offset = jumps[current_pos]
        new_pos = current_pos + offset
        jumps[current_pos] = offset + (-1 if offset >= 3 else + 1)
        current_pos = new_pos
        steps = steps + 1
    print(f"part 2 answer: {steps}")


if __name__ == "__main__":
    with open("aoc/2017/Day05/input.txt") as f:
        jumps = [int(s) for s in f.readlines()]
        part1(jumps.copy())
        part2(jumps.copy())
