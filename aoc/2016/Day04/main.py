from itertools import groupby
from operator import itemgetter
import re


def part1(lines):
    total = 0
    for line in lines:
        result = re.match(r"^(.*)-(\d+)\[(.*)\]", line)
        name, sector, expected_checksum = result.group(1, 2, 3)
        letters = sorted(name.replace('-', ''))
        grouped_1 = groupby(letters)
        grouped_2 = [(k, -len(list(v))) for k, v in grouped_1]
        grouped_3 = sorted(grouped_2, key=itemgetter(1, 0))
        grouped_4 = [k for k, _ in grouped_3[:5]]
        calculated_checksum = ''.join(grouped_4)
        if calculated_checksum == expected_checksum:
            total = total + int(sector)
    print(f"part 1 answer: {total}")


def part2(lines):
    print(f"part 2 answer: {0}")


if __name__ == "__main__":
    with open("aoc/2016/Day04/input.txt") as f:
        lines = f.readlines()
        part1(lines)
        part2(lines)
