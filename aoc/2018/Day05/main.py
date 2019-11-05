def find_reacting_units(polymer):
    for pos in range(len(polymer) - 1):
        code1 = ord(polymer[pos])
        code2 = ord(polymer[pos + 1])
        if abs(code1 - code2) == 32: return pos
    return None


def part1(polymer):
    while True:
        pos = find_reacting_units(polymer)
        print(f"pos: {pos}")
        if pos is None: break
        polymer = polymer[:pos] + polymer[pos + 2:]
    print(f"part 1 answer: {len(polymer)}")


if __name__ == "__main__":
    with open("aoc/2018/Day05/input.txt") as f:
        polymer = f.read().rstrip()
        part1(polymer)
