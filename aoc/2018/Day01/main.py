def part1(numbers):
    total = sum(numbers)
    print(f"part 1 answer: {total}")


def part2(numbers):
    current_pos = 0
    total = 0
    seen_totals = set()
    while True:
        number = numbers[current_pos % len(numbers)]
        current_pos = current_pos + 1
        total = total + number
        if total in seen_totals:
            print(f"part 2 answer: {total}")
            break
        seen_totals.add(total)


if __name__ == "__main__":
    with open("aoc/2018/Day01/input.txt") as f:
        numbers = [int(s) for s in f.readlines()]
        part1(numbers)
        part2(numbers)
