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


def make_pos_dict(claims):
    d = defaultdict(list)
    for claim in claims:
        for pos in get_claim_coords(claim):
            claim_id = claim[0]
            d[pos].append(claim_id)
    return d


def part1(claims):
    d = make_pos_dict(claims)
    total_overlap = sum([1 for value in d.values() if len(value) > 1])
    print(f"part 1 answer: {total_overlap}")


def part2(claims):
    d = make_pos_dict(claims)
    values = d.values()
    for claim in claims:
        claim_id = claim[0]
        if all([len(v) == 1 for v in values if claim_id in v]):
            print(f"part 2 answer: {claim_id}")
            break


if __name__ == "__main__":
    with open("aoc/2018/Day03/input.txt") as f:
        claims = [parse_line(line) for line in f.readlines()]
        part1(claims)
        part2(claims)
