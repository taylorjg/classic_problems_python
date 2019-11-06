import re


def find_reacting_units(polymer, start):
    for pos in range(start, len(polymer) - 1):
        code1 = ord(polymer[pos])
        code2 = ord(polymer[pos + 1])
        if abs(code1 - code2) == 32: return pos
    return None


def react_polymer(polymer):
    start = 0
    while True:
        pos = find_reacting_units(polymer, start)
        if pos is None: break
        polymer = polymer[:pos] + polymer[pos + 2:]
        start = max(0, pos - 1)
    return polymer


def part1(polymer):
    shortest_polymer = react_polymer(polymer)
    print(f"part 1 answer: {len(shortest_polymer)}")


def make_new_polymer(polymer, letter):
    return re.sub(letter, "", polymer, flags=re.IGNORECASE)


def part2(polymer):
    letters = set(str.lower(polymer))
    new_polymers = [make_new_polymer(polymer, l) for l in letters]
    reacted_lengths = [len(react_polymer(np)) for np in new_polymers]
    sorted_lengths = sorted(reacted_lengths)
    print(f"part 2 answer: {sorted_lengths[0]}")


if __name__ == "__main__":
    with open("aoc/2018/Day05/input.txt") as f:
        polymer = f.read().rstrip()
        part1(polymer)
        part2(polymer)
