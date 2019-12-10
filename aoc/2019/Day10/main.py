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


def find_asteroid_pts(lines, width, height):
    asteroid_pts = []
    for y in range(height):
        for x in range(width):
            if lines[y][x] == "#":
                asteroid_pts.append((x, y))
    return asteroid_pts


def part1(lines):
    width = len(lines[0])
    height = len(lines)
    asteroid_pts = find_asteroid_pts(lines, width, height)
    counts = [get_asteroid_counts(asteroid_pts, asteroid_pt) for asteroid_pt in asteroid_pts]
    print(counts)
    sorted_counts = sorted(counts, key=lambda t: t[1], reverse=True)
    print(sorted_counts)
    answer = sorted_counts[0][1]
    print(f"part 1 answer: {answer}")


if __name__ == "__main__":
#     data = """
# .#..#
# .....
# #####
# ....#
# ...##
# """
#     lines1 = [line.rstrip() for line in data.split("\n")]
#     lines2 = [line for line in lines1 if len(line) > 0]
#     print(lines2)
#     part1(lines2)
    with open("aoc/2019/Day10/input.txt") as f:
        lines = [line.rstrip() for line in f.readlines()]
        part1(lines)
