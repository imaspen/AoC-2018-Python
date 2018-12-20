import itertools
from collections import defaultdict

__author__ = "Aspen Thompson"
__date__ = "17-12-2018"


DOWN = 0+1j
UP = 0-1j
LEFT = -1+0j
RIGHT = 1+0j


def get_grid(veins):
    min_x = min([vein.min_x() for vein in veins])
    min_y = min([vein.min_y() for vein in veins])
    max_x = max([vein.max_x() for vein in veins])
    max_y = max([vein.max_y() for vein in veins])
    grid = defaultdict(lambda: defaultdict(int))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            grid[y][x] = 0
    for vein in veins:
        for y in vein.y_range():
            for x in vein.x_range():
                grid[y][x] = 1
    return dict(grid)


def print_grid(grid):
    for row in grid.values():
        for cell in row.values():
            print("#" if cell == 1 else '~' if cell == 2 else '|' if cell == 3 else '.', end="")
        print()
    print()


def get_propagated_grid(grid, min_y):
    n = {(500, min_y,)}
    while len(n) > 0:
        d = Drop(grid, *n.pop())
        n = n | d.live()
        del d
    return grid


def part_one(lines):
    veins = [Vein.from_string(line) for line in lines]
    grid = get_propagated_grid(get_grid(veins), min([vein.min_y() for vein in veins]))
    score = sum(itertools.chain(*[[1 for cell in row.values() if cell in [2, 3]] for row in grid.values()]))
    print_grid(grid)
    return score


def part_two(lines):
    pass


class Drop:
    def __init__(self, grid, x=500, y=0):
        self.grid = grid
        self.x = x
        self.y = y
        self.grid[self.y][self.x] = 2

    def spread(self, l, r, t):
        for x in range(l, r + 1):
            self.grid[self.y][x] = t

    def live(self):
        new_drops = set()
        while self.y < max(self.grid.keys()) and self.grid[self.y + 1][self.x] not in [1, 2]:
            self.grid[self.y][self.x] = 3
            self.y += 1
            self.grid[self.y][self.x] = 2
        if self.y < max(self.grid.keys()):
            lx = self.x
            rx = self.x
            t = 2
            while self.grid[self.y][lx - 1] in [0, 3]:
                lx -= 1
                if self.grid[self.y + 1][lx] in [0, 3]:
                    t = 3
                    new_drops.add((lx, self.y,))
                    break
            while self.grid[self.y][rx + 1] in [0, 3]:
                rx += 1
                if self.grid[self.y + 1][rx] in [0, 3]:
                    t = 3
                    new_drops.add((rx, self.y,))
                    break
            if len(new_drops) == 0:
                new_drops.add((self.x, self.y - 1,))
            self.spread(lx, rx, t)
        else:
            self.grid[self.y][self.x] = 3
        return new_drops


class Vein:
    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Vein.VERTICAL if type(x) == int else Vein.HORIZONTAL

    def x_range(self):
        return self.x if self.direction == Vein.HORIZONTAL else range(self.x, self.x + 1)

    def y_range(self):
        return self.y if self.direction == Vein.VERTICAL else range(self.y, self.y + 1)

    def min_x(self):
        return self.x if self.direction == Vein.VERTICAL else min(self.x)

    def min_y(self):
        return self.y if self.direction == Vein.HORIZONTAL else min(self.y)

    def max_x(self):
        return self.x if self.direction == Vein.VERTICAL else max(self.x)

    def max_y(self):
        return self.y if self.direction == Vein.HORIZONTAL else max(self.y)

    @staticmethod
    def from_string(line):
        parts = line.split(', ')
        p_one = int(parts[0][2:])
        p_two = parts[1].split('..')
        p_two = range(int(p_two[0][2:]), int(p_two[1]) + 1)
        x = 0
        y = 0
        if parts[0][0] == 'x':
            x = p_one
            y = p_two
        else:
            x = p_two
            y = p_one
        return Vein(x, y)

    def __repr__(self):
        return "Vein(x: {}, y: {}, dir: {})".format(self.x, self.y, self.direction)
