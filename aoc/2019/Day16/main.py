from itertools import chain, cycle

BASE_PATTERN = [0, 1, 0, -1]


def get_pattern_cycle(one_based_position):
    one_cycle = chain(*[[v] * one_based_position for v in BASE_PATTERN])
    for idx, value in enumerate(cycle(one_cycle)):
        if idx == 0:
            continue
        yield value


def calc_digit(signal, idx):
    pattern_cycle = get_pattern_cycle(idx + 1)
    pairs = zip(signal, pattern_cycle)
    total = sum([a * b for a, b in pairs])
    return int(str(total)[-1])


def apply_phase(signal):
    for idx in range(len(signal)):
        signal[idx] = calc_digit(signal, idx)


def part1(signal_str):
    signal = [int(ch) for ch in signal_str.rstrip()]
    for _ in range(100):
        apply_phase(signal)
    answer = "".join([str(digit) for digit in signal[:8]])
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day16/input.txt") as f:
        part1(f.read())
