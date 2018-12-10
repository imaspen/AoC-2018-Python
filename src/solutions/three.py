from collections import defaultdict
from itertools import chain

__author__ = "Aspen Thompson"
__date__ = "2018-12-03"


def part_one(claims):
    fabric = defaultdict(lambda: defaultdict(int))
    for claim_str in claims:
        claim = Claim(claim_str)
        for x in range(claim.x_pos, claim.x_pos + claim.width):
            for y in range(claim.y_pos, claim.y_pos + claim.height):
                fabric[x][y] += 1

    count = 0
    for row in fabric.values():
        for cell in row.values():
            if cell > 1:
                count += 1
    return count


def part_two(claims):
    claims_len = len(claims)
    for i in range(claims_len):
        claim = Claim(claims[i])
        collided = False
        for j in chain(range(0, i), range(i + 1, claims_len)):
            test = Claim(claims[j])
            if claim.overlaps(test):
                collided = True
                break
        if not collided:
            return claim.id


class Claim:
    def __init__(self, claim):
        claim_parts = claim.split()
        self.id = int(claim_parts[0][1:])
        pos = claim_parts[2].split(",")
        self.x_pos = int(pos[0])
        self.y_pos = int(pos[1][:-1])
        dimensions = claim_parts[3].split("x")
        self.width = int(dimensions[0])
        self.height = int(dimensions[1])

    def get_left(self):
        return self.x_pos

    def get_bottom(self):
        return self.y_pos

    def get_right(self):
        return self.x_pos + self.width - 1

    def get_top(self):
        return self.y_pos + self.height - 1

    def overlaps(self, claim):
        if self.get_right() < claim.get_left():
            return False
        if self.get_left() > claim.get_right():
            return False
        if self.get_top() < claim.get_bottom():
            return False
        if self.get_bottom() > claim.get_top():
            return False
        return True
