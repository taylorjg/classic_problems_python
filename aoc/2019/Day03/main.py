def advance(pos, direction, distance):
    x, y = pos
    ds = range(1, distance + 1)
    if direction == "U": return [(x, y + d) for d in ds]
    if direction == "D": return [(x, y - d) for d in ds]
    if direction == "L": return [(x - d, y) for d in ds]
    if direction == "R": return [(x + d, y) for d in ds]


def find_path(wire):
    pos = 0, 0
    path = [pos]
    for instruction in wire:
        direction = instruction[0]
        distance = int(instruction[1:])
        new_positions = advance(pos, direction, distance)
        pos = new_positions[-1]
        path = path + new_positions
    return path


def find_crossings(path1, path2):
    s1 = set(path1[1:])
    s2 = set(path2[1:])
    return s1.intersection(s2)


def manhattan_distance(pos):
    x, y = pos
    return abs(x) + abs(y)


def count_steps(path, pos):
    count = 0
    while True:
        if path[count] == pos:
            break
        count = count + 1
    return count


def combined_steps(path1, path2, crossing):
    steps1 = count_steps(path1, crossing)
    steps2 = count_steps(path2, crossing)
    return steps1 + steps2


def part1(crossings):
    answer = sorted([manhattan_distance(crossing) for crossing in crossings])[0]
    print(f"part 1 answer: {answer}")


def part2(path1, path2, crossings):
    answer = sorted([combined_steps(path1, path2, crossing) for crossing in crossings])[0]
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day03/input.txt") as f:
        line1 = f.readline()
        line2 = f.readline()
        wire1 = line1.rstrip().split(',')
        wire2 = line2.rstrip().split(',')
        path1 = find_path(wire1)
        path2 = find_path(wire2)
        crossings = find_crossings(path1, path2)
        part1(crossings)
        part2(path1, path2, crossings)
