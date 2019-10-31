N = 0
E = 1
S = 2
W = 3


def calc_distance(pos):
    x, y = pos
    return abs(x) + abs(y)


def move(pos, direction, distance):
    x, y = pos
    if direction == N: return x, y + distance
    if direction == S: return x, y - distance
    if direction == E: return x + distance, y
    if direction == W: return x - distance, y


def part1(instructions):
    current_pos = 0, 0
    direction = N
    for instruction in instructions:
        distance = int(instruction[1:])
        if instruction[0] == "L": direction = (direction - 1) % 4
        if instruction[0] == "R": direction = (direction + 1) % 4
        current_pos = move(current_pos, direction, distance)
    print(f"part 1 answer: {calc_distance(current_pos)}")


def move_locations(pos, direction, distance):
    x, y = pos
    ds = range(1, distance + 1)
    if direction == N: return [(x, y + d) for d in ds]
    if direction == S: return [(x, y - d) for d in ds]
    if direction == E: return [(x + d, y) for d in ds]
    if direction == W: return [(x - d, y) for d in ds]


def part2(instructions):
    direction = N
    visited = [(0, 0)]
    for instruction in instructions:
        distance = int(instruction[1:])
        if instruction[0] == "L": direction = (direction - 1) % 4
        if instruction[0] == "R": direction = (direction + 1) % 4
        current_pos = visited[-1]
        locations = move_locations(current_pos, direction, distance)
        for location in locations:
            if location in visited:
                print(f"part 2 answer: {calc_distance(location)}")
                return
        visited.extend(locations)


if __name__ == "__main__":
    with open("aoc/2016/Day01/input.txt") as f:
        chars = f.read()
        instructions = chars.split(", ")
        part1(instructions)
        part2(instructions)
