from itertools import groupby


def meets_criteria(number):
    s = str(number)
    return len(set(s)) < 6 and s == "".join(sorted(s))


def part1(numbers):
    numbers_meeting_criteria = filter(meets_criteria, numbers)
    answer = len(list(numbers_meeting_criteria))
    print(f"part 1 answer: {answer}")


def has_double_digit(number):
    s = str(number)
    groups = groupby(s)
    lengths = [len(list(v)) for _, v in groups]
    num_twos = lengths.count(2)
    return num_twos >= 1


def part2(numbers):
    numbers_meeting_criteria = filter(meets_criteria, numbers)
    answer = len(list(filter(has_double_digit, numbers_meeting_criteria)))
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    numbers = range(145852, 616942 + 1)
    part1(numbers)
    part2(numbers)
