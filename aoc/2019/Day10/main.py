import math

# From Beautiful Code, Page 549
# (defun area-collinear (px py qx qy rx ry)
#   (= (* (- px rx) (- qy ry))
#      (* (- qx rx) (- py ry))))

EPSILON = 1e-12


def points_are_collinear(p, q, r):
    px, py = p
    qx, qy = q
    rx, ry = r
    term1 = (px - rx) * (qy - ry)
    term2 = (qx - rx) * (py - ry)
    delta = abs(term1 - term2)
    return delta < EPSILON


def get_points_in_rect(pts, source, target):
    sx, sy = source
    tx, ty = target
    minx = min(sx, tx)
    maxx = max(sx, tx)
    miny = min(sy, ty)
    maxy = max(sy, ty)
    result = []
    for pt in pts:
        x, y = pt
        if minx <= x <= maxx and miny <= y <= maxy and pt != source and pt != target:
            result.append(pt)
    return result


def get_asteroid_counts(asteroid_pts, source):
    other_asteroid_pts = [pt for pt in asteroid_pts if pt != source]
    detected = set()
    for target in other_asteroid_pts:
        inbetween_pts = get_points_in_rect(other_asteroid_pts, source, target)
        collinear_count = 0
        for inbetween_pt in inbetween_pts:
            if points_are_collinear(source, inbetween_pt, target):
                collinear_count = collinear_count + 1
                break
        if collinear_count == 0:
            detected.add(target)
    return source, len(detected)


def find_asteroid_pts(lines):
    width = len(lines[0])
    height = len(lines)
    asteroid_pts = []
    for y in range(height):
        for x in range(width):
            if lines[y][x] == "#":
                asteroid_pts.append((x, y))
    return asteroid_pts


def part1(asteroid_pts):
    counts = [get_asteroid_counts(asteroid_pts, asteroid_pt) for asteroid_pt in asteroid_pts]
    sorted_counts = sorted(counts, key=lambda t: t[1], reverse=True)
    answer = sorted_counts[0][1]
    print(f"part 1 answer: {answer}")


def part2(asteroid_pts):
    counts = [get_asteroid_counts(asteroid_pts, asteroid_pt) for asteroid_pt in asteroid_pts]
    sorted_counts = sorted(counts, key=lambda t: t[1], reverse=True)
    station = sorted_counts[0][0]
    sx, sy = station

    # We want something a bit like Polar coordinates but
    # going clockwise instead of counterclockwise and
    # with 0 degrees pointing North instead of East. Also, we
    # need to take account of the Y axis increasing downwards.
    def pt_angle(pt):
        px, py = pt
        x = px - sx
        y = sy - py
        angle1 = math.degrees(math.atan2(y, x))
        angle2 = angle1 + 360 if angle1 < 0 else angle1
        angle3 = (360 - angle2 + 90) % 360
        return angle3

    def pt_distance(pt):
        px, py = pt
        x = px - sx
        y = sy - py
        return x * x + y * y

    pt_data = sorted([(pt_angle(pt), pt_distance(pt), pt) for pt in asteroid_pts], key=lambda t: (t[0], t[1]))

    vaporised = []
    while len(pt_data):
        angle, distance, pt = pt_data.pop(0)
        vaporised.append(pt)
        # move asteroids with the same angle to the end of the list
        ts = [t for t in pt_data if t[0] == angle]
        for t in ts:
            pt_data.pop(0)
            pt_data.append(t)
    x, y = vaporised[199]
    answer = x * 100 + y
    print(f"part 2 answer: {answer}")


if __name__ == "__main__":
    with open("aoc/2019/Day10/input.txt") as f:
        lines = [line.rstrip() for line in f.readlines()]
        asteroid_pts = find_asteroid_pts(lines)
        part1(asteroid_pts)
        part2(asteroid_pts)
