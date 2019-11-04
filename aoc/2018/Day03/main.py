import re
from collections import defaultdict
from itertools import product


def parse_line(line):
    result = re.match(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)\n", line)
    claim_id, x, y, w, h = map(int, result.group(1, 2, 3, 4, 5))
    return claim_id, x, y, w, h


def get_claim_coords(claim):
    _, x, y, w, h = claim
    xs = range(x, x + w)
    ys = range(y, y + h)
    return product(xs, ys)


def part1(claims):
    d = defaultdict(int)
    for claim in claims:
        for pos in get_claim_coords(claim):
            d[pos] = d[pos] + 1
    total_overlap = sum([1 for value in d.values() if value > 1])
    print(f"part 1 answer: {total_overlap}")


def part2(claims):
    print(f"part 1 answer: {0}")


if __name__ == "__main__":
    with open("aoc/2018/Day03/input.txt") as f:
        claims = [parse_line(line) for line in f.readlines()]
        part1(claims)
        part2(claims)
