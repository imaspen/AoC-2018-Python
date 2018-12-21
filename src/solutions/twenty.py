import itertools
import math
from collections import defaultdict

__author__ = "Aspen Thompson"
__date__ = "2018-12-20"


def print_grid(grid):
    min_x = min([min(l.keys()) for l in grid.values()])
    max_x = max([max(l.keys()) for l in grid.values()])
    for y in range(min(grid.keys()), max(grid.keys()) + 1):
        l1 = l2 = '#'
        for x in range(min_x, max_x + 1):
            l1 += ('.' if (x, y) != (0, 0) else 'X') \
                  + ('|' if grid[y][x].e else '#')
            l2 += ('-' if grid[y][x].s else '#') + '#'
        print(l1)
        print(l2)


def generate_grid(line):
    grid = defaultdict(lambda: defaultdict(Node))
    moves = {'N': 0 - 1j, 'E': 1 + 0j, 'S': 0 + 1j, 'W': -1 + 0j}
    opp = {'N': 'S', 'S': 'N', 'W': 'E', 'E': 'W'}
    c = 0 + 0j
    sub_groups = []
    for char in line[1:-1]:
        if char == '(':
            sub_groups.append(c)
        elif char == '|':
            c = sub_groups[-1]
        elif char == ')':
            sub_groups.pop()
        else:
            grid[int(c.imag)][int(c.real)].grid = grid
            grid[int(c.imag)][int(c.real)].y = int(c.imag)
            grid[int(c.imag)][int(c.real)].x = int(c.real)
            if char == 'N':
                grid[int(c.imag)][int(c.real)].n = True
                c += moves[char]
                grid[int(c.imag)][int(c.real)].s = True
            elif char == 'E':
                grid[int(c.imag)][int(c.real)].e = True
                c += moves[char]
                grid[int(c.imag)][int(c.real)].w = True
            elif char == 'S':
                grid[int(c.imag)][int(c.real)].s = True
                c += moves[char]
                grid[int(c.imag)][int(c.real)].n = True
            elif char == 'W':
                grid[int(c.imag)][int(c.real)].w = True
                c += moves[char]
                grid[int(c.imag)][int(c.real)].e = True
            grid[int(c.imag)][int(c.real)].grid = grid
            grid[int(c.imag)][int(c.real)].y = int(c.imag)
            grid[int(c.imag)][int(c.real)].x = int(c.real)
    return grid


def get_len(paths):
    for i in range(len(paths)):
        if type(paths[i]) == list:
            paths[i] = get_len(paths[i])
        else:
            paths[i] = 1
    return sum(paths)


def part_one(line):
    grid = generate_grid(line)
    return max(
        itertools.chain(*[r.values() for r in grid[0][0].get_paths().values()])
        , key=lambda n: n.d
    )


def part_two(line):
    pass


class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.grid = None
        self.n = False
        self.e = False
        self.s = False
        self.w = False
        self.parent = None
        self.d = math.inf

    @property
    def neighbors(self):
        return [val for val in [
            None if not self.n else self.grid[self.y - 1][self.x],
            None if not self.e else self.grid[self.y][self.x + 1],
            None if not self.s else self.grid[self.y + 1][self.x],
            None if not self.w else self.grid[self.y][self.x - 1],
        ] if val is not None]

    def get_paths(self):
        q = set(itertools.chain(*[r.values() for r in self.grid.values()]))
        for v in q:
            v.parent = None
            v.d = math.inf
        self.d = 0
        while len(q) > 0:
            u = min(q, key=lambda node: node.d)
            q.remove(u)
            for neighbor in u.neighbors:
                if neighbor in q:
                    alt = u.d + 1
                    if alt < neighbor.d:
                        neighbor.d = alt
                        neighbor.parent = u
        return self.grid

    def __repr__(self):
        return "Node(x: {}, y: {}, d: {})".format(self.x, self.y, self.d)
