from math import floor, sqrt
from itertools import count, product


# https://metacpan.org/pod/Math::PlanePath::SquareSpiral
def n_to_xy(n):
    d = floor((1 + sqrt(n - 1)) / 2)
    nsig = n - (4 * d ** 2 + 1)
    if nsig <= -2 * d: return d, 3 * d + nsig
    if -2 * d <= nsig <= 0: return -d - nsig, d
    if 0 <= nsig <= 2 * d: return -d, d - nsig
    if 2 * d <= nsig: return nsig - 3 * d, -d


def manhattan_distance(x, y):
    return abs(x) + abs(y)


def part1(n):
    x, y = n_to_xy(n)
    print(f"part 1 answer: {manhattan_distance(x, y)}")


def get_neighbours(xy_to_values, x, y):
    xs = range(x - 1, x + 2)
    ys = range(y - 1, y + 2)
    return [pos for pos in product(xs, ys) if pos != (x, y) and pos in xy_to_values]


def part2(target):
    xy_to_values = {(0, 0): 1}
    for n in count(2):
        x, y = n_to_xy(n)
        neighbours = get_neighbours(xy_to_values, x, y)
        total = sum([xy_to_values[neighbour] for neighbour in neighbours])
        xy_to_values[x, y] = total
        if total > target:
            print(f"part 2 answer: {total}")
            break


if __name__ == "__main__":
    puzzle_input = 289326
    part1(puzzle_input)
    part2(puzzle_input)
