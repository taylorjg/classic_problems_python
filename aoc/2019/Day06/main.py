import sys

sys.path.insert(0, '.')

from book.chapter2.generic_search import bfs, node_to_path
from functools import partial

COM = "COM"


def get_orbit_count(nodes, name, count=0):
    if name == COM:
        return count
    else:
        return get_orbit_count(nodes, nodes[name], count + 1)


def part1(nodes):
    answer = sum([get_orbit_count(nodes, name) for name in nodes.keys()])
    print(f"part 1 answer: {answer}")


def successors(nodes, name):
    objects_orbiting_this_object = [k for k, v in nodes.items() if v == name]
    objects_orbited_by_this_object = [] if name == COM else [nodes[name]]
    return objects_orbiting_this_object + objects_orbited_by_this_object


def part2(nodes):
    start = nodes["YOU"]
    goal = nodes["SAN"]
    node = bfs(start, lambda name: name == goal, partial(successors, nodes))
    path = node_to_path(node)
    print(f"part 2 answer: {len(path) - 1}")


if __name__ == "__main__":
    with open("aoc/2019/Day06/input.txt") as f:
        orbits = [s.rstrip() for s in f.readlines()]
        nodes = {}
        for orbit in orbits:
            [parent, child] = orbit.split(")")
            nodes[child] = parent
        part1(nodes)
        part2(nodes)
