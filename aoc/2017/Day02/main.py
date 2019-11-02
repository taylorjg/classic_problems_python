import itertools


def part1(lines):
    checksum = 0
    for line in lines:
        numbers = [int(s) for s in line.split()]
        biggest = max(numbers)
        smallest = min(numbers)
        difference = biggest - smallest
        checksum = checksum + difference
    print(f"part 1 answer: {checksum}")


def part2(lines):
    total = 0
    for line in lines:
        numbers = [int(s) for s in line.split()]
        for combination in itertools.combinations(numbers, 2):
            biggest = max(combination)
            smallest = min(combination)
            q, r = divmod(biggest, smallest)
            if r == 0:
                total = total + q
                break
    print(f"part 2 answer: {total}")


if __name__ == "__main__":
    with open("aoc/2017/Day02/input.txt") as f:
        lines = f.readlines()
        part1(lines)
        part2(lines)
