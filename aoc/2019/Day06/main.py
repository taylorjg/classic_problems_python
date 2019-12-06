COM = "COM"


def get_orbit_count(nodes, name, count=0):
    return count if name == COM else get_orbit_count(nodes, nodes[name], count + 1)


def part1(nodes):
    answer = sum([get_orbit_count(nodes, name) for name in nodes.keys()])
    print(f"part 1 answer: {answer}")


def part2(nodes):
    print(f"part 2 answer: {0}")


if __name__ == "__main__":
    with open("aoc/2019/Day06/input.txt") as f:
        orbits = [s.rstrip() for s in f.readlines()]
        nodes = {}
        for orbit in orbits:
            [parent, child] = orbit.split(")")
            nodes[child] = parent
        part1(nodes)
        part2(nodes)
