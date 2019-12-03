def advance(pos, direction, distance):
    x, y = pos
    ds = range(1, distance + 1)
    if direction == "U": return [(x, y + d) for d in ds]
    if direction == "D": return [(x, y - d) for d in ds]
    if direction == "L": return [(x - d, y) for d in ds]
    if direction == "R": return [(x + d, y) for d in ds]


def find_path(wire):
    path = []
    pos = 0, 0
    for instruction in wire:
        direction = instruction[0]
        distance = int(instruction[1:])
        new_positions = advance(pos, direction, distance)
        pos = new_positions[-1]
        path = path + new_positions
    return path


def find_crossings(path1, path2):
    s1 = set(path1)
    s2 = set(path2)
    return s1.intersection(s2)


def manhattan_distance(pos):
    x, y = pos
    return abs(x) + abs(y)


def find_nearest_crossing(crossings):
    return sorted([manhattan_distance(crossing) for crossing in crossings])[0]


def part1(wire1, wire2):
    path1 = find_path(wire1)
    path2 = find_path(wire2)
    crossings = find_crossings(path1, path2)
    answer = find_nearest_crossing(crossings)
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
    # line1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    # line2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    # wire1 = line1.rstrip().split(',')
    # wire2 = line2.rstrip().split(',')
    # part1(wire1, wire2)
    with open("aoc/2019/Day03/input.txt") as f:
        line1 = f.readline()
        line2 = f.readline()
        wire1 = line1.rstrip().split(',')
        wire2 = line2.rstrip().split(',')
        part1(wire1, wire2)
