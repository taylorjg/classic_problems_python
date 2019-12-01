def calc_fuel(m):
    return m // 3 - 2


def calc_fuel_including_fuel(m):
    total = calc_fuel(m)
    fuel = calc_fuel(total)
    while True:
        if fuel <= 0:
            break
        total = total + fuel
        fuel = calc_fuel(fuel)
    return total


def part1(ms):
    answer = sum([calc_fuel(m) for m in ms])
    print(f"part 1 answer: {answer}")


def part2(ms):
    answer = sum([calc_fuel_including_fuel(m) for m in ms])
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day01/input.txt") as f:
        modules = [int(s) for s in f.readlines()]
        part1(modules)
        part2(modules)
