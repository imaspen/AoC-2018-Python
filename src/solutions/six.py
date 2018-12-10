from collections import Counter, defaultdict
from itertools import chain

__author__ = "Aspen Thompson"
__date__ = "2018-12-06"


def get_points(lines):
    return [tuple([int(c) for c in line.split(", ")]) for line in lines]


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_min(distances):
    distances.sort(key=lambda d: d[0])
    if distances[0][0] != distances[1][0]:
        return distances[0][1]
    else:
        return -1


def get_max_area(counts, inclusions):
    max_area = 0
    for i in inclusions:
        if counts[i] > max_area:
            max_area = counts[i]
    return max_area


def part_one(lines):
    points = get_points(lines)
    top = min(points, key=lambda point: point[1])[1] - 1
    left = min(points, key=lambda point: point[0])[0] - 1
    bottom = max(points, key=lambda point: point[1])[1] + 1
    right = max(points, key=lambda point: point[0])[0] + 1

    distances = defaultdict(lambda: defaultdict(int))
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            d = [(distance((x, y), point), i,) for i, point in enumerate(points)]
            distances[x][y] = get_min(d)

    all_points = set(range(len(points)))
    infinite = set()
    for x in range(left, right):
        infinite.add(distances[x][top])
        infinite.add(distances[x][bottom])
    for y in range(top, bottom):
        infinite.add(distances[left][y])
        infinite.add(distances[right][y])

    counts = Counter(chain.from_iterable([d.values() for d in distances.values()]))

    return get_max_area(counts, all_points - infinite)


def part_two(lines):
    points = get_points(lines)
    top = min(points, key=lambda point: point[1])[1] - 1
    left = min(points, key=lambda point: point[0])[0] - 1
    bottom = max(points, key=lambda point: point[1])[1] + 1
    right = max(points, key=lambda point: point[0])[0] + 1

    count = 0
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            d = [distance((x, y), point) for point in points]
            if sum(d) < 10000:
                count += 1
    return count
