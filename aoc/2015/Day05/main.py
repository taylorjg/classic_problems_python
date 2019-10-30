import itertools


def part1_check_1(s):
    return len([c for c in s if c in "aeiou"]) >= 3


def part1_check_2(s):
    grouped = itertools.groupby(s)
    lengths = [len(list(v)) for _, v in grouped]
    return [length > 1 for length in lengths].count(True) > 0


def part1_check_3(s):
    disallowed_pairs = ["ab", "cd", "pq", "xy"]
    return len([dp for dp in disallowed_pairs if dp in s]) == 0


def passes_all_part1_checks(s):
    fns = [
        part1_check_1,
        part1_check_2,
        part1_check_3
    ]
    return all([fn(s) for fn in fns])


def part2_check_1(s):
    for pos in range(len(s)):
        pair = s[pos:pos + 2]
        if pair in s[pos + 2:]: return True
    return False


def part2_check_2(s):
    for pos in range(len(s)):
        letters = s[pos:pos + 3]
        if len(letters) == 3:
            [a, _, b] = letters
            if a == b: return True
    return False


def passes_all_part2_checks(s):
    fns = [
        part2_check_1,
        part2_check_2
    ]
    return all([fn(s) for fn in fns])


def part1(ss):
    answer = [passes_all_part1_checks(s) for s in ss].count(True)
    print(f"part 1 answer: {answer}")


def part2(ss):
    answer = [passes_all_part2_checks(s) for s in ss].count(True)
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2015/Day05/input.txt") as f:
        strings = f.readlines()
        part1(strings)
        part2(strings)
