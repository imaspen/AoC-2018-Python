from solutions.fifteen.node import Node
from solutions.fifteen.unit import Unit

__author__ = "Aspen Thompson"
__date__ = "2018-12-15"

GOBLIN = 'GOBLIN'
ELF = 'ELF'
FLOOR = 'FLOOR'
WALL = 'WALL'


def print_grid(grid):
    library = {
        WALL: '#',
        FLOOR: '.',
        GOBLIN: 'G',
        ELF: 'E'
    }
    for row in grid:
        for cell in row:
            print(library[cell.mode], end="")
        print()
    print()


def generate_grid(lines):
    grid = []
    library = {
        '#': lambda _x, _y, _grid: Node(_x, _y, _grid, WALL),
        '.': lambda _x, _y, _grid: Node(_x, _y, _grid, FLOOR),
        'G': lambda _x, _y, _grid: Unit(_x, _y, _grid, GOBLIN),
        'E': lambda _x, _y, _grid: Unit(_x, _y, _grid, ELF)
    }
    for y, line in enumerate(lines):
        grid.append([])
        for x, char in enumerate(line):
            grid[-1].append(library[char](x, y, grid))
    return grid


def part_one(lines):
    i = 0
    grid = generate_grid(lines)
    while True:
        move_order = []
        for row in grid:
            for cell in row:
                if type(cell) == Unit:
                    move_order.append(cell)
        for unit in move_order:
            print(unit)
            if unit.hp > 0:
                if not unit.take_turn():
                    total_hp = 0
                    for row in grid:
                        for cell in row:
                            if type(cell) == Unit:
                                total_hp += cell.hp
                    print(i)
                    print_grid(grid)
                    print(total_hp)
                    return i * total_hp
        i += 1
        print(i)
        print_grid(grid)
