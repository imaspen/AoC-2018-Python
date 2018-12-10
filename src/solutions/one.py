import itertools

__author__ = "Aspen Thompson"
__date__ = "2018-12-01"


def part_one(frequencies):
    count = 0
    for x in frequencies:
        count += x
    return count


def part_two(frequencies):
    running = {0}
    frequency = 0
    for x in itertools.cycle(frequencies):
        frequency += x
        if frequency in running:
            return frequency
        else:
            running.add(frequency)
