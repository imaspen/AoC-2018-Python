import numpy

__author__ = "Aspen Thompson"
__date__ = "2018-12-11"


def get_grid(serial_number):
    def get_val(x, y):
        rack_id = x + 11
        return ((((rack_id * (y + 1) + serial_number)
                  * rack_id) // 100) % 10) - 5

    return numpy.fromfunction(get_val, (300, 300,))


def part_one(serial_number):
    grid = get_grid(serial_number)
    max_group = (0, (0, 0,),)
    for y in range(298):
        for x in range(298):
            total = numpy.sum(grid[x:x+3, y:y+3])
            if total > max_group[0]:
                max_group = (total, (x + 1, y + 1,),)
    return max_group


def part_two(serial_number):
    grid = get_grid(serial_number)
    max_group = (0, (0, 0, 0,),)
    for size in range(1, 301):
        for y in range(301 - size):
            for x in range(301 - size):
                total = numpy.sum(grid[x:x+size, y:y+size])
                if total > max_group[0]:
                    max_group = (total, (x + 1, y + 1, size,),)
        print(size, max_group)
    return max_group
