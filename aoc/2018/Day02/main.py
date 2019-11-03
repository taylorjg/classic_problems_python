from itertools import groupby


def part1(box_ids):
    twos = 0
    threes = 0
    for box_id in box_ids:
        grouped_letters = groupby(sorted(box_id))
        lengths = [len(list(letters)) for _, letters in grouped_letters]
        twos = twos + (2 in lengths)
        threes = threes + (3 in lengths)
    checksum = twos * threes
    print(f"part 1 answer: {checksum}")


def part2(box_ids):
    for box_id_1 in box_ids:
        for box_id_2 in box_ids:
            matching_chars = [c for i, c in enumerate(box_id_1) if c == box_id_2[i]]
            if len(matching_chars) == len(box_id_1) - 1:
                print(f"part 2 answer: {''.join(matching_chars)}")
                return


if __name__ == "__main__":
    with open("aoc/2018/Day02/input.txt") as f:
        box_ids = [s.rstrip() for s in f.readlines()]
        part1(box_ids)
        part2(box_ids)
