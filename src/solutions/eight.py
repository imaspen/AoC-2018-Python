__author__ = "Aspen Thompson"
__date__ = "2018-12-08"


def get_tree(ints, i=0):
    node = Member()
    num_children = ints[i]
    num_metadata = ints[i + 1]
    i += 2
    while len(node.children) < num_children:
        child, i = get_tree(ints, i)
        node.children.append(child)
    while len(node.metadata) < num_metadata:
        node.metadata.append(ints[i])
        i += 1
    return node, i


def part_one(ints):
    return get_tree(ints)[0].metadata_total()


def part_two(ints):
    return get_tree(ints)[0].get_value()


class Member:
    def __init__(self):
        self.metadata = []
        self.children = []

    def metadata_total(self):
        total = 0
        for child in self.children:
            total += child.metadata_total()
        return total + sum(self.metadata)

    def get_value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        else:
            total = 0
            for i in self.metadata:
                if i <= len(self.children):
                    total += self.children[i - 1].get_value()
            return total
