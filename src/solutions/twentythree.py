import z3

__author__ = "Aspen Thompson"
__date__ = "2018-12-23"


def get_bots(lines):
    def parse_line(line):
        p = line.split(", ")
        return Nanobot(*[int(i) for i in p[0][5:-1].split(",")], int(p[1][2:]))
    return [parse_line(line) for line in lines]


def part_one(lines):
    bots = get_bots(lines)
    main = max(bots, key=lambda bot: bot.r)
    return sum([main.is_point_in_range(b.x, b.y, b.z) for b in bots])


def part_two(lines):
    bots = get_bots(lines)
    optimizer = z3.Optimize()
    zx = z3.Int('x')
    zy = z3.Int('y')
    zz = z3.Int('z')
    zc = z3.Int('c')
    zd = z3.Int('d')

    def zabs(x):
        return z3.If(x >= 0, x, -x)

    for bot in bots:
        optimizer.add(bot.zoverlaps == z3.If(
            zabs(zx - bot.x) + zabs(zy - bot.y) + zabs(zz - bot.z) <= bot.r,
            1, 0
        ))
    optimizer.add(zc == sum([bot.zoverlaps for bot in bots]))
    optimizer.add(zd == zabs(zx) + zabs(zy) + zabs(zz))

    optimizer.maximize(zc)
    z_min_distance = optimizer.minimize(zd)

    optimizer.check()
    return optimizer.upper(z_min_distance)


class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.zr = z3.Int("r")
        self.overlaps = set()
        self.zoverlaps = z3.Int(f"overlaps-{x}-{y}")

    def is_point_in_range(self, x, y, z):
        return (abs(x - self.x) + abs(y - self.y) + abs(z - self.z)) <= self.r
    
    def __repr__(self):
        return f"Nanobot(x: {self.x}, y: {self.y}, z: {self.z}, r: {self.r})"
