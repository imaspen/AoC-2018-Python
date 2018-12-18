class Node:
    def __init__(self, x, y, grid, mode):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.d = 0
        self.grid = grid
        self.mode = mode
        self.parent = None

    @property
    def f(self):
        return self.g + self.h

    @property
    def neighbors(self):
        return [
            None if self.y == 0 else self.grid[self.y - 1][self.x],
            None if self.x == 0 else self.grid[self.y][self.x - 1],
            None if self.x == len(self.grid[0]) - 1 else self.grid[self.y][self.x + 1],
            None if self.y == len(self.grid) - 1 else self.grid[self.y + 1][self.x]
        ]
