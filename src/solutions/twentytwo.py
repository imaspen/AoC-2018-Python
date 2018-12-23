import itertools
import math
from functools import lru_cache

__author__ = "Aspen Thompson"
__date__ = "2018-12-22"


@lru_cache(None)
def g_index(x, y, target, depth):
    if (x, y,) == (0, 0,):
        return 0
    elif (x, y,) == target:
        return 0
    elif y == 0:
        return ((x * 16807) + depth) % 20183
    elif x == 0:
        return ((y * 48271) + depth) % 20183
    else:
        return ((g_index(x - 1, y, target, depth)
                 * g_index(x, y - 1, target, depth)) + depth) % 20183


def e_level(x, y, target, depth):
    return g_index(x, y, target, depth) % 3


def part_one(lines):
    depth = int(lines[0].split(" ")[1])
    target = tuple([int(p) for p in lines[1].split(" ")[1].split(",")])
    return sum(
        e_level(x, y, target, depth)
        for x in range(target[0] + 1)
        for y in range(target[1] + 1)
    )


def part_two(lines):
    depth = int(lines[0].split(" ")[1])
    target = tuple([int(p) for p in lines[1].split(" ")[1].split(",")])
    grid = []
    for y in range(target[1] + 100):
        grid.append([])
        for x in range(target[0] + 50):
            e = e_level(x, y, target, depth)
            grid[-1].append([])
            if e != 0:
                grid[-1][-1].append(Node(x, y, e, 0, grid))
            if e != 1:
                grid[-1][-1].append(Node(x, y, e, 1, grid))
            if e != 2:
                grid[-1][-1].append(Node(x, y, e, 2, grid))

    return grid[0][0][0].get_path(grid[target[1]][target[0]][0])


class Node:
    def __init__(self, x, y, e, tool, grid):
        self.x = x
        self.y = y
        self.d = math.inf
        self.parent = None
        self.e = e
        self.tool = tool
        self.grid = grid

    def valid_at_x_y(self, x, y):
        if x < 0 or y < 0 or x >= len(self.grid[0]) or y >= len(self.grid):
            return None
        else:
            return [
                cell for cell in self.grid[y][x] if cell.tool == self.tool]

    @property
    def neighbors(self):
        return itertools.chain(*[
            val for val in [
                self.valid_at_x_y(self.x, self.y - 1),
                self.valid_at_x_y(self.x + 1, self.y),
                self.valid_at_x_y(self.x, self.y + 1),
                self.valid_at_x_y(self.x - 1, self.y),
                [self.grid[self.y][self.x][
                    0 if self.grid[self.y][self.x][0] != self else 1
                ]]
            ] if val is not None
        ])

    def get_path(self, target):
        q = set([self.grid[y][x][i] for y in range(len(self.grid))
                 for x in range(len(self.grid[0])) for i in range(2)])
        non_inf = {self}

        for cell in q:
            cell.d = math.inf
            cell.parent = None
        self.d = 0
        self.parent = None

        while len(q) > 0:
            u = min(non_inf, key=lambda node: node.d)
            if u == target:
                break
            q.remove(u)
            non_inf.remove(u)
            for neighbor in u.neighbors:
                if neighbor in q:
                    alt = u.d + (1 if u.tool == neighbor.tool else 7)
                    non_inf.add(neighbor)
                    if alt < neighbor.d:
                        neighbor.d = alt
                        neighbor.parent = u
            if len(q) % 100 == 0:
                print(len(q))
        current = target
        return target.d
