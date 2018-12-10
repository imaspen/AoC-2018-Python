__author__ = "Aspen Thompson"
__date__ = "2018-12-10"


def part_one(points):
    points = [Point.from_string(point) for point in points]
    seconds_passed = 0
    while (min(points, key=lambda point: point.position[1]).position[1] + 9
           < max(points, key=lambda point: point.position[1]).position[1]):
        for point in points:
            point.step()
        seconds_passed += 1

    canvas_left = min(points, key=lambda point: point.position[0]).position[0]
    canvas_right = max(points, key=lambda point: point.position[0]).position[0]
    canvas_bottom = min(points, key=lambda point: point.position[1]).position[1]
    canvas_top = max(points, key=lambda point: point.position[1]).position[1]

    for y in range(canvas_bottom, canvas_top + 1):
        for x in range(canvas_left, canvas_right + 1):
            to_print = " "
            for point in points:
                if point.position == (x, y):
                    to_print = "#"
                    break
            print(to_print, end="")
        print()

    return seconds_passed

class Point:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def step(self, steps=1):
        self.position = (self.position[0] + (self.velocity[0] * steps),
                         self.position[1] + (self.velocity[1] * steps))

    @staticmethod
    def string_to_vector(string):
        return tuple([int(val) for val in string.split(',')])

    @staticmethod
    def from_string(string):
        parts = string.split("> velocity=<")
        return Point(Point.string_to_vector(parts[0][10:]),
                     Point.string_to_vector(parts[1][:-1]))
