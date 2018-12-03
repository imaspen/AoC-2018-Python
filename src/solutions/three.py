from collections import defaultdict
import string

__author__ = "Aspen Thompson"


def part_one(claims):
    fabric = defaultdict(lambda: defaultdict(list))
    for claim_str in claims:
        claim = Claim(claim_str)


class Claim:
    def __init__(self, claim):
        """
        :type claim: string
        """
        claim_parts = claim.split()
        self.id = int(claim_parts[0][1:])
        pos = claim_parts[2].split(",")
        self.x_pos = int(pos[0])
        self.y_pos = int(pos[1][:1])
        dimensions = claim_parts[3].split("x")
        self.width = int(dimensions[0])
        self.height = int(dimensions[1])
