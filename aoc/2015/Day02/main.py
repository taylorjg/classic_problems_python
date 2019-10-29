import re


def part1(lines):
    total = 0
    for line in lines:
        result = re.match(r"^(\d+)x(\d+)x(\d+)\n", line)
        l, w, h = map(int, result.group(1, 2, 3))
        surface_areas = [2 * l * w, 2 * w * h, 2 * h * l]
        extra = min(surface_areas) // 2
        total = total + sum(surface_areas) + extra
    print(f"part 1 answer: {total}")


def part2(lines):
    total = 0
    for line in lines:
        result = re.match(r"^(\d+)x(\d+)x(\d+)\n", line)
        l, w, h = map(int, result.group(1, 2, 3))
        [d0, d1, _] = sorted([l, w, h])
        perimeter = d0 + d0 + d1 + d1
        volume = l * w * h
        total = total + perimeter + volume
    print(f"part 2 answer: {total}")


if __name__ == "__main__":
    with open("aoc/2015/Day02/input.txt") as f:
        lines = f.readlines()
        part1(lines)
        part2(lines)
