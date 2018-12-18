import itertools
import math

from solutions.fifteen.node import Node

FLOOR = "FLOOR"


class Unit(Node):
    def __init__(self, x, y, grid, mode, hp=200, ap=3):
        Node.__init__(self, x, y, grid, mode)
        self._hp = hp
        self.ap = ap

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value <= 0:
            self.grid[self.y][self.x] = Node(self.x, self.y, self.grid, FLOOR)
        else:
            self._hp = value

    @property
    def enemy_neighbors(self):
        return [unit for unit in self.neighbors if type(unit) == Unit and unit.mode != self.mode]

    def is_cell_enemy(self, cell):
        return type(cell) == Unit and cell.mode != self.mode

    def take_turn(self):
        targets = [cell for cell in itertools.chain(*self.grid) if self.is_cell_enemy(cell)]
        if len(targets) == 0:
            return False
        else:
            paths = []
            if not self.attack():
                for target in targets:
                    move_targets = [self.get_path(node) for node in target.neighbors if node.mode == FLOOR]
                    routes = [path for path in move_targets if path is not None]
                    if len(routes) > 0:
                        paths.append(min(routes, key=lambda route: (len(route), route[-1].y, route[-1].x)))
                if len(paths) > 0:
                    path = min(paths, key=lambda path: (len(path), path[-1].y, path[-1].x))
                    self.move(path[-1])
                self.attack()
        return True

    def move(self, target):
        self.grid[target.y][target.x] = self
        self.grid[self.y][self.x] = target
        tx = self.x
        ty = self.y
        self.x = target.x
        self.y = target.y
        target.x = tx
        target.y = ty

    def attack(self):
        if len(self.enemy_neighbors) > 0:
            min(self.enemy_neighbors, key=lambda unit: (unit.hp, unit.y, unit.x)).hp -= self.ap
            return True
        return False

    def get_path_a(self, target):
        open_list = {self}
        closed_list = set()
        while target not in closed_list:
            if len(open_list) == 0:
                return None
            current = min(open_list, key=lambda node: node.f)
            open_list.remove(current)
            closed_list.add(current)
            if target in closed_list:
                break
            for i, neighbor in enumerate(current.neighbors):
                if (type(neighbor) == Node and neighbor.mode == FLOOR
                        and neighbor not in closed_list or neighbor == target):
                    if neighbor not in open_list:
                        neighbor.parent = current
                        neighbor.g = current.g + 1
                        neighbor.h = (abs(neighbor.x - target.x) + abs(neighbor.y - target.y))
                        open_list.add(neighbor)
                    elif current.g + 1 < neighbor.g:
                        neighbor.g = current.g + 1
                        neighbor.parent = current

        path = [target]
        while path[-1].parent.parent is not None:
            path.append(path[-1].parent)
        return path

    def get_path(self, target):
        q = set([cell for cell in itertools.chain(*self.grid) if cell.mode == FLOOR])

        for cell in q:
            cell.d = math.inf
            cell.parent = None
        self.d = 0
        self.parent = None

        q.add(self)

        while len(q) > 0:
            u = min(q, key=lambda node: node.d)
            if u == target:
                break
            q.remove(u)
            for neighbor in u.neighbors:
                if neighbor in q:
                    alt = u.d + 1
                    if alt < neighbor.d:
                        neighbor.d = alt
                        neighbor.parent = u
                    elif alt == neighbor.d and alt != math.inf:
                        if (u.y < neighbor.parent.y) or (u.y == neighbor.parent.y and u.x < neighbor.parent.x):
                            neighbor.parent = u

        if target.parent is None:
            return None
        path = [target]
        while path[-1].parent.parent is not None:
            path.append(path[-1].parent)
        return path

    def __str__(self):
        return "Unit(x: {}, y: {}, d: {}, team: {}, hp: {})".format(self.x, self.y, self.d, self.mode, self.hp)

    def __repr__(self):
        return "Unit(x: {}, y: {}, d: {}, team: {}, hp: {})".format(self.x, self.y, self.d, self.mode, self.hp)
