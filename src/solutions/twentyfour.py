import re

__author__ = "Aspen Thompson"
__date__ = "2018-12-24"


def get_units(lines, boost=0):
    a = set()
    b = set()
    current = 'a'
    for line in lines[1:]:
        if line == "Infection:":
            current = 'b'
        elif line != "":
            if current == 'a':
                n = Unit.from_string(current[0], line, boost)
                a.add(n)
            else:
                n = Unit.from_string(current[0], line)
                b.add(n)
    return a, b


def set_targets(a, b):
    us = set(b)
    for unit in sorted(a, key=lambda u: (u.ap * u.count, u.initiative),
                       reverse=True):
        if len(us) == 0:
            break
        unit.target = max(
            us, key=lambda u: (u.count > 0, u.get_damage(unit), u.ep,
                               u.initiative)
        )
        if unit.target.get_damage(unit) <= 0 or unit.count <= 0 or \
                unit.target.count <= 0:
            unit.target = None
        else:
            us.remove(unit.target)


def do_attacks(a, b):
    for unit in sorted(a.union(b), key=lambda u: u.initiative, reverse=True):
        if unit.count > 0:
            unit.attack()


def get_alive(units):
    return sum([unit.count for unit in units if unit.count > 0])


def part_one(lines):
    a, b = get_units(lines)
    while get_alive(a) > 0 and get_alive(b) > 0:
        set_targets(a, b)
        set_targets(b, a)
        do_attacks(a, b)
    return max(get_alive(a), get_alive(b))


def part_two(lines):
    a, b = get_units(lines, 79)
    while get_alive(a) > 0 and get_alive(b) > 0:
        set_targets(a, b)
        set_targets(b, a)
        do_attacks(a, b)
    if get_alive(b) > 0:
        return False
    return get_alive(a)


class Unit:
    def __init__(self):
        self.team = ""
        self.count = 0
        self.hp = 0
        self.immunities = set()
        self.weaknesses = set()
        self.ap = 0
        self.damage_type = ""
        self.initiative = 0
        self.target = None

    @property
    def ep(self):
        return self.count * self.ap

    def get_damage(self, unit):
        return unit.ep * (
            0 if unit.damage_type in self.immunities else
            2 if unit.damage_type in self.weaknesses else 1
        )

    def attack(self):
        if self.target is not None:
            self.target.count -= self.target.get_damage(self) // self.target.hp

    @staticmethod
    def from_string(team, string, boost=0):
        u = Unit()
        u.team = team
        r = re.compile(
            "^(?P<count>\d+) units each with (?P<hp>\d+) hit points "
            "(?:\((?:(?:(?:(?:immune to (?P<immunities>(?:\w*(?:, )?)+))?)"
            "|(?:weak to (?P<weaknesses>(?:\w*(?:, )?)+)?)?)(?:; )?){1,2}\) )?"
            "with an attack that does (?P<ap>\d+) (?P<type>\w+) damage at "
            "initiative (?P<initiative>\d+)$"
        )
        p = r.search(string)
        p = p.groupdict()
        u.count = int(p['count'])
        u.hp = int(p['hp'])
        u.immunities = p['immunities'].split(", ")\
            if p['immunities'] is not None else []
        u.weaknesses = p['weaknesses'].split(", ")\
            if p['weaknesses'] is not None else []
        u.ap = int(p['ap']) + boost
        u.damage_type = p['type']
        u.initiative = int(p['initiative'])
        return u

    def __repr__(self):
        return (f"Unit(t: {self.team}, c: {self.count}, hp: {self.hp}, "
                f"i: {self.immunities}, w: {self.weaknesses}, "
                f"ap: {self.ap}, t: {self.damage_type}, i: {self.initiative})")
