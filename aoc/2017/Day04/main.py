from itertools import groupby


def part1(lines):
    valid_count = 0
    for line in lines:
        sorted_words = sorted(line.split())
        grouped = groupby(sorted_words)
        len1 = len(sorted_words)
        len2 = len(list(grouped))
        if len1 == len2:
            valid_count = valid_count + 1
    print(f"part 1 answer: {valid_count}")


def part2(lines):
    valid_count = 0
    for line in lines:
        sorted_words = sorted(["".join(sorted(word)) for word in line.split()])
        grouped = list(groupby(sorted_words))
        if len(sorted_words) == len(grouped):
            valid_count = valid_count + 1
    print(f"part 2 answer: {valid_count}")


if __name__ == "__main__":
    with open("aoc/2017/Day04/input.txt") as f:
        lines = f.readlines()
        part1(lines)
        part2(lines)
