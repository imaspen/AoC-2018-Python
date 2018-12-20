import itertools

__author__ = "Aspen Thompson"
__date__ = "2018-12-18"


def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()


def next_grid(grid):
    def get_neighbors(_x, _y):
        neighbors = []
        left_edge = _x == 0
        right_edge = _x == len(grid[0]) - 1
        top_edge = _y == 0
        bottom_edge = _y == len(grid) - 1
        if not left_edge:
            neighbors.append(grid[_y][_x - 1])
            if not top_edge:
                neighbors.append(grid[_y - 1][_x - 1])
            if not bottom_edge:
                neighbors.append(grid[_y + 1][_x - 1])
        if not right_edge:
            neighbors.append(grid[_y][_x + 1])
            if not top_edge:
                neighbors.append(grid[_y - 1][_x + 1])
            if not bottom_edge:
                neighbors.append(grid[_y + 1][_x + 1])
        if not top_edge:
            neighbors.append(grid[_y - 1][_x])
        if not bottom_edge:
            neighbors.append(grid[_y + 1][_x])

        return neighbors

    g = []
    for y, row in enumerate(grid):
        g.append([])
        for x, cell in enumerate(row):
            ns = get_neighbors(x, y)
            if cell == '.':
                g[y].append(
                    '|' if sum([1 for n in ns if n == '|']) >= 3 else '.'
                )
            elif cell == '|':
                g[y].append(
                    '#' if sum([1 for n in ns if n == '#']) >= 3 else '|'
                )
            else:
                g[y].append(
                    '#' if '#' in ns and '|' in ns else '.'
                )
    return g


def get_score(grid):
    return sum([1 for cell in itertools.chain(*grid) if cell == "#"]) * sum(
        [1 for cell in itertools.chain(*grid) if cell == "|"])


def part_one(grid):
    for i in range(10):
        grid = next_grid(grid)
    print_grid(grid)
    return get_score(grid)


def part_two(grid):
    seen = []
    skipped = False
    i = 0
    while i < 1000000000:
        grid = next_grid(grid)
        n = (i, get_score(grid),)
        matches = [c for c in seen if c[1] == n[1]]
        if skipped:
            i += 1
        else:
            if len(matches) >= 5:
                diff = matches[-1][0] - matches[-2][0]
                if diff == matches[-2][0] - matches[-3][0] == matches[-3][0]\
                        - matches[-4][0]:
                    while i < 1000000000:
                        i += diff
                    i -= diff - 1
                    skipped = True
            else:
                seen.append(n)
                i += 1
    print_grid(grid)
    return sum([1 for cell in itertools.chain(*grid) if cell == "#"]) * sum(
        [1 for cell in itertools.chain(*grid) if cell == "|"])
