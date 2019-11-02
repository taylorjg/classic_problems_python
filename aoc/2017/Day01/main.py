def part1(numbers):
    length = len(numbers)
    total = 0
    for index, number in enumerate(numbers):
        next_index = (index + 1) % length
        if numbers[next_index] == number:
            total = total + int(number)
    print(f"part 1 answer: {total}")


def part2(numbers):
    length = len(numbers)
    half_length = length // 2
    total = 0
    for index, number in enumerate(numbers):
        next_index = (index + half_length) % length
        if numbers[next_index] == number:
            total = total + int(number)
    print(f"part 2 answer: {total}")


if __name__ == "__main__":
    with open("aoc/2017/Day01/input.txt") as f:
        numbers = f.read().rstrip()
        part1(numbers)
        part2(numbers)
