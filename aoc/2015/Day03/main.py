def move(pos, direction):
    x, y = pos
    if direction == "^": return x, y + 1
    if direction == "v": return x, y - 1
    if direction == "<": return x - 1, y
    if direction == ">": return x + 1, y
    raise ValueError(f"Unknown direction, {direction}.")


def part1(directions):
    current_pos = 0, 0
    visited = set(current_pos)
    for direction in directions:
        current_pos = move(current_pos, direction)
        visited.add(current_pos)
    print(f"part 1 answer: {len(visited)}")


def part2(directions):
    santa_count = 2
    starting_pos = 0, 0
    current_pos = [starting_pos for _ in range(santa_count)]
    visited = [{starting_pos} for _ in range(santa_count)]
    for index, direction in enumerate(directions):
        turn = index % santa_count
        current_pos[turn] = move(current_pos[turn], direction)
        visited[turn].add(current_pos[turn])
    print(f"part 2 answer: {len(set.union(*visited))}")


if __name__ == "__main__":
    with open("aoc/2015/Day03/input.txt") as f:
        directions = f.read()
        part1(directions)
        part2(directions)
