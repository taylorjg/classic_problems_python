import numpy as np


def part1(chars):
    lparens = chars.count("(")
    rparens = chars.count(")")
    print(f"part 1 answer: {abs(lparens - rparens)}")


def part2(chars):
    def ch_to_step(ch):
        if ch == "(": return 1
        if ch == ")": return -1
        raise ValueError(f"Unknown char {ch}.")

    data = np.array([ch_to_step(ch) for ch in chars])
    basement_indexes, = (data.cumsum() == -1).nonzero()
    print(f"part 2 answer: {basement_indexes[0] + 1}")


if __name__ == "__main__":
    with open("aoc/2015/Day01/input.txt") as f:
        chars = f.read()
        part1(chars)
        part2(chars)
