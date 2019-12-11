import math


# From Beautiful Code, Page 549
# (defun area-collinear (px py qx qy rx ry)
#   (= (* (- px rx) (- qy ry))
#      (* (- qx rx) (- py ry))))

def points_are_collinear(p, q, r):
    px, py = p
    qx, qy = q
    rx, ry = r
    term1 = (px - rx) * (qy - ry)
    term2 = (qx - rx) * (py - ry)
    return term1 - term2 == 0


def get_asteroids_in_rect(asteroids, source, target):
    sx, sy = source
    tx, ty = target
    minx = min(sx, tx)
    maxx = max(sx, tx)
    miny = min(sy, ty)
    maxy = max(sy, ty)
    result = []
    for asteroid in asteroids:
        if asteroid == source or asteroid == target:
            continue
        x, y = asteroid
        if minx <= x <= maxx and miny <= y <= maxy:
            result.append(asteroid)
    return result


def get_detected_counts(asteroids, source):
    detected = set()
    for target in asteroids:
        if target == source:
            continue
        inbetweens = get_asteroids_in_rect(asteroids, source, target)
        collinear_found = False
        for inbetween in inbetweens:
            if points_are_collinear(source, inbetween, target):
                collinear_found = True
                break
        if not collinear_found:
            detected.add(target)
    return source, len(detected)


def find_asteroids(lines):
    width = len(lines[0])
    height = len(lines)
    asteroids = []
    for y in range(height):
        for x in range(width):
            if lines[y][x] == "#":
                asteroids.append((x, y))
    return asteroids


def part1(detected_counts):
    answer = detected_counts[0][1]
    print(f"part 1 answer: {answer}")


def part2(detected_counts, asteroids):
    station = detected_counts[0][0]
    sx, sy = station

    # We want something a bit like Polar coordinates but
    # going clockwise instead of counterclockwise and
    # with 0 degrees pointing North instead of East. Also, we
    # need to take account of the Y axis increasing downwards.
    # Use the station as the origin.
    def calc_angle(asteroid):
        ax, ay = asteroid
        x = ax - sx
        y = sy - ay
        angle1 = math.degrees(math.atan2(y, x))
        angle2 = angle1 + 360 if angle1 < 0 else angle1
        angle3 = (360 - angle2 + 90) % 360
        return angle3

    def calc_distance(asteroid):
        ax, ay = asteroid
        x = ax - sx
        y = sy - ay
        return x * x + y * y

    data = [(calc_angle(asteroid), calc_distance(asteroid), asteroid) for asteroid in asteroids]
    sorted_data = sorted(data, key=lambda t: (t[0], t[1]))

    vaporised = []
    while len(sorted_data):
        angle, distance, asteroid = sorted_data.pop(0)
        vaporised.append(asteroid)
        # move asteroids with the same angle to the end of the list
        ts = [t for t in sorted_data if t[0] == angle]
        for t in ts:
            sorted_data.pop(0)
            sorted_data.append(t)
    x, y = vaporised[199]
    answer = x * 100 + y
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day10/input.txt") as f:
        lines = [line.rstrip() for line in f.readlines()]
        asteroids = find_asteroids(lines)
        detected_counts = [get_detected_counts(asteroids, asteroid) for asteroid in asteroids]
        sorted_detected_counts = sorted(detected_counts, key=lambda t: t[1], reverse=True)
        part1(sorted_detected_counts)
        part2(sorted_detected_counts, asteroids)
