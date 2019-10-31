def triangle_is_valid(sides):
    [a, b, c] = sides
    combs = [[a, b, c], [a, c, b], [b, c, a]]
    return all([x + y > z for [x, y, z] in combs])


def count_valid_triangles(triangles):
    return [triangle_is_valid(triangle) for triangle in triangles].count(True)


def parse_line(line):
    return [int(s) for s in line.split()]


def part1(lines):
    triangles = [parse_line(line) for line in lines]
    num_valid = count_valid_triangles(triangles)
    print(f"part 1 answer: {num_valid}")


def part2(lines):
    triangles = []
    for index in range(0, len(lines), 3):
        [l1, l2, l3] = lines[index:index + 3]
        [a1, b1, c1] = parse_line(l1)
        [a2, b2, c2] = parse_line(l2)
        [a3, b3, c3] = parse_line(l3)
        triangles.extend([[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]])
    num_valid = count_valid_triangles(triangles)
    print(f"part 2 answer: {num_valid}")


if __name__ == "__main__":
    with open("aoc/2016/Day03/input.txt") as f:
        lines = f.readlines()
        part1(lines)
        part2(lines)
