from itertools import combinations, count
from functools import reduce
from math import gcd
import re


def pad(n):
    return str(n).rjust(4)


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def energy(self):
        vs = [self.x, self.y, self.z]
        return sum([abs(v) for v in vs])

    def __getitem__(self, item):
        if item == "x": return self.x
        if item == "y": return self.y
        if item == "z": return self.z
        raise TypeError(f"[Vector] unknown item {item}.")

    def __str__(self):
        return f"<x={pad(self.x)}, y={pad(self.y)}, z={pad(self.z)}>"


class Moon:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel

    def energy(self):
        return self.pos.energy() * self.vel.energy()

    def __str__(self):
        return f"pos={str(self.pos)}, vel={str(self.vel)}"


def apply_gravity_to_pair(moon1, moon2):
    def calc_pull(a, b):
        if b > a: return +1
        if a > b: return -1
        return 0

    pull_x = calc_pull(moon1.pos.x, moon2.pos.x)
    pull_y = calc_pull(moon1.pos.y, moon2.pos.y)
    pull_z = calc_pull(moon1.pos.z, moon2.pos.z)

    moon1.vel.x += pull_x
    moon1.vel.y += pull_y
    moon1.vel.z += pull_z

    moon2.vel.x += -pull_x
    moon2.vel.y += -pull_y
    moon2.vel.z += -pull_z


def apply_gravity(moons):
    combs = combinations(moons, 2)
    for moon1, moon2 in combs:
        apply_gravity_to_pair(moon1, moon2)


def apply_velocity(moons):
    for moon in moons:
        moon.pos.x += moon.vel.x
        moon.pos.y += moon.vel.y
        moon.pos.z += moon.vel.z


def time_step(moons):
    apply_gravity(moons)
    apply_velocity(moons)


def part1(positions):
    moons = [Moon(Vector(x, y, z), Vector(0, 0, 0)) for x, y, z in positions]
    for _ in range(1000): time_step(moons)
    answer = sum([moon.energy() for moon in moons])
    print(f"part 1 answer: {answer}")


def make_state(m, axis):
    return m.pos[axis], m.vel[axis]


def find_cycle_periods(positions):
    moons = [Moon(Vector(x, y, z), Vector(0, 0, 0)) for x, y, z in positions]
    start_state_x = [make_state(moon, "x") for moon in moons]
    start_state_y = [make_state(moon, "y") for moon in moons]
    start_state_z = [make_state(moon, "z") for moon in moons]
    periods = []
    for step in count(1):
        time_step(moons)
        state_x = [make_state(moon, "x") for moon in moons]
        state_y = [make_state(moon, "y") for moon in moons]
        state_z = [make_state(moon, "z") for moon in moons]
        if state_x == start_state_x: periods.append(step)
        if state_y == start_state_y: periods.append(step)
        if state_z == start_state_z: periods.append(step)
        if len(periods) == 3: return periods


def lcm(a, b):
    return a * b // gcd(a, b)


def lcms(numbers):
    return reduce(lcm, numbers)


def part2(positions):
    periods = find_cycle_periods(positions)
    answer = lcms(periods)
    print(f"part 2 answer: {answer}")


def parse_line(line):
    result = re.match(r"^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$", line.rstrip())
    x, y, z = map(int, result.group(1, 2, 3))
    return x, y, z


if __name__ == "__main__":
    with open("aoc/2019/Day12/input.txt") as f:
        lines = f.readlines()
        positions = [parse_line(line) for line in lines]
        part1(positions)
        part2(positions)
