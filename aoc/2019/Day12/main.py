from itertools import combinations
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
    def delta(a, b):
        if b > a:
            return +1
        if a > b:
            return -1
        return 0

    delta_x = delta(moon1.pos.x, moon2.pos.x)
    delta_y = delta(moon1.pos.y, moon2.pos.y)
    delta_z = delta(moon1.pos.z, moon2.pos.z)
    moon1.vel.x = moon1.vel.x + delta_x
    moon1.vel.y = moon1.vel.y + delta_y
    moon1.vel.z = moon1.vel.z + delta_z
    moon2.vel.x = moon2.vel.x + (-delta_x)
    moon2.vel.y = moon2.vel.y + (-delta_y)
    moon2.vel.z = moon2.vel.z + (-delta_z)


def apply_gravity(moons):
    combs = combinations(moons, 2)
    for moon1, moon2 in combs:
        apply_gravity_to_pair(moon1, moon2)


def apply_velocity(moons):
    for moon in moons:
        moon.pos.x = moon.pos.x + moon.vel.x
        moon.pos.y = moon.pos.y + moon.vel.y
        moon.pos.z = moon.pos.z + moon.vel.z


def time_step(moons):
    apply_gravity(moons)
    apply_velocity(moons)


def dump_moons(moons):
    for moon in moons:
        print(moon)
    print()


def part1(moons):
    for _ in range(1000):
        time_step(moons)
    total_energy = sum([moon.energy() for moon in moons])
    print(f"part 1 answer: {total_energy}")


def parseLine(line):
    result = re.match(r"^<x=(-?\d+), y=(-?\d+), z=(-?\d+)>$", line.rstrip())
    x, y, z = map(int, result.group(1, 2, 3))
    return x, y, z


if __name__ == "__main__":
    with open("aoc/2019/Day12/input.txt") as f:
        lines = f.readlines()
        positions = [parseLine(line) for line in lines]
        moons = [Moon(Vector(x, y, z), Vector(0, 0, 0)) for x, y, z in positions]
        part1(moons)
