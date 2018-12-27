__author__ = "Aspen Thompson"
__date__ = "2018-12-25"


def get_star_field(lines):
    field = set()
    for line in lines:
        field.add(Node.from_string(line, field))
    return field


def get_constellation(start, field):
    constellation = {start}
    unconsidered = set(field)
    unconsidered.remove(start)
    last_length = len(unconsidered)
    while True:
        for star in field:
            if star in unconsidered and len(
                    [1 for s in constellation if star in s.close]) > 0:
                constellation.add(star)
                unconsidered.remove(star)
        if len(unconsidered) == last_length:
            break
        else:
            last_length = len(unconsidered)
    return constellation


def part_one(lines):
    field = get_star_field(lines)
    unmatched = set(field)
    constellations = []
    while len(unmatched) > 0:
        c = get_constellation(list(unmatched)[0], unmatched)
        unmatched = unmatched.difference(c)
        constellations.append(c)
    return len(constellations)


def part_two(lines):
    pass


class Node:
    def __init__(self, c, field):
        self.c = c
        self.field = field
        self.__close = None

    def get_dist(self, target):
        return (
            abs(self.c[0] - target.c[0]) +
            abs(self.c[1] - target.c[1]) +
            abs(self.c[2] - target.c[2]) +
            abs(self.c[3] - target.c[3])
        )

    @property
    def close(self):
        if self.__close is None:
            self.__close = set([star for star in self.field if
                                self.get_dist(star) <= 3 and star != self])
        return self.__close

    @staticmethod
    def from_string(string, field):
        return Node(tuple([int(i) for i in string.split(",")]), field)

    def __repr__(self):
        return f"Node(c: {self.c})"
