import itertools

vowels = "aeiou"


def has_three_vowels(s):
    return len([c for c in s if c in vowels]) >= 3


def has_repeated_letter(s):
    grouped = itertools.groupby(s)
    lengths = [len(list(v)) for _, v in grouped]
    return [length > 1 for length in lengths].count(True) > 0


def has_no_disallowed_pairs(s):
    disallowed_pairs = ["ab", "cd", "pq", "xy"]
    return len([dp for dp in disallowed_pairs if dp in s]) == 0


def passes_all_checks(s):
    fns = [
        has_three_vowels,
        has_repeated_letter,
        has_no_disallowed_pairs
    ]
    return all([fn(s) for fn in fns])


def part1(ss):
    answer = [passes_all_checks(s) for s in ss].count(True)
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2015/Day05/input.txt") as f:
        strings = f.readlines()
        part1(strings)
