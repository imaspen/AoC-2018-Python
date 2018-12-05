__author__ = "Aspen Thompson"


def part_one(polymer):
    i = 0
    while i + 1 < len(polymer):
        if polymer[i].upper() == polymer[i + 1].upper() and polymer[i] != polymer[i + 1]:
            polymer = polymer.replace(polymer[i] + polymer[i + 1], "", 1)
            i -= 1
            if i < 0:
                i = 0
            continue
        i += 1
    return len(polymer)


def part_two(polymer):
    min_len = len(polymer)
    for c in range(ord('a'), ord('z')):
        char = chr(c)
        length = part_one(polymer.replace(char, "").replace(char.upper(), ""))
        if length < min_len:
            min_len = length
    return min_len
