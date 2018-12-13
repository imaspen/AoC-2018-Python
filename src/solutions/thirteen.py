import itertools
from collections import defaultdict

__author__ = "Aspen Thompson"
__date__ = "2018-12-13"


def parse_input(lines):
    grid = []
    carts = []
    for y, line in enumerate(lines):
        grid.append([])
        for x, char in enumerate(line):
            if char == '^':
                grid[y].append('|')
                carts.append(Cart(x, y, 0))
            elif char == '>':
                grid[y].append('-')
                carts.append(Cart(x, y, 1))
            elif char == 'v':
                grid[y].append('|')
                carts.append(Cart(x, y, 2))
            elif char == '<':
                grid[y].append('-')
                carts.append(Cart(x, y, 3))
            else:
                grid[y].append(char)
    return grid, carts


def part_one(lines):
    grid, carts = parse_input(lines)
    while True:
        carts.sort(key=lambda c: (c.x, c.y))
        for i, cart in enumerate(carts):
            cart.step(grid)
            for test_cart in itertools.chain(carts[:i], carts[i+1:]):
                if test_cart.x == cart.x and test_cart.y == cart.y:
                    return cart.x, cart.y


def part_two(lines):
    grid, carts = parse_input(lines)
    while True:
        carts.sort(key=lambda c: (c.x, c.y))
        for i, cart in enumerate(carts):
            cart.step(grid)
            for test_cart in itertools.chain(carts[:i], carts[i+1:]):
                if test_cart.x == cart.x and test_cart.y == cart.y:
                    test_cart.alive = False
                    cart.alive = False
        carts = [cart for cart in carts if cart.alive]
        if len(carts) == 1:
            return carts[0].x, carts[0].y


class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turns = 0
        self.alive = True

    def turn(self, track):
        if track == '+':
            if self.turns == 0:
                self.direction -= 1
            elif self.turns == 2:
                self.direction += 1
            self.turns = (self.turns + 1) % 3
            self.direction = self.direction % 4
        elif self.direction == 0:
            if track == '\\':
                self.direction = 3
            elif track == '/':
                self.direction = 1
        elif self.direction == 1:
            if track == '/':
                self.direction = 0
            elif track == '\\':
                self.direction = 2
        elif self.direction == 2:
            if track == '\\':
                self.direction = 1
            elif track == '/':
                self.direction = 3
        elif self.direction == 3:
            if track == '/':
                self.direction = 2
            elif track == '\\':
                self.direction = 0

    def step(self, grid):
        track = grid[self.y][self.x]
        self.turn(track)

        if self.direction == 0:
            self.y -= 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y += 1
        elif self.direction == 3:
            self.x -= 1

    def __str__(self):
        return "dir={}, x={}, y={}".format(self.direction, self.x, self.y)
