import itertools
from collections import defaultdict

__author__ = "Aspen Thomspon"
__date__ = "2018-12-19"


def get_program(lines):
    return [[line.split(" ")[0], *[int(i) for i in line.split(" ")[1:]]] for line in lines]


def part_one(lines):
    ip = int(lines[0][-1])
    instructions = get_program(lines[1:])
    cpu = Cpu()
    while cpu.registers[ip] in range(len(instructions)):
        cpu.execute(instructions[cpu.registers[ip]])
        cpu.registers[ip] += 1
    return cpu.registers[0]


def part_two(lines):
    """Find the sum of all factors of an input"""
    ip = int(lines[0][-1])
    instructions = get_program(lines[1:])
    cpu = Cpu()
    cpu.registers[0] = 1
    while cpu.registers[ip] != 1:
        cpu.execute(instructions[cpu.registers[ip]])
        cpu.registers[ip] += 1
    n = cpu.registers[4]
    a = sum(itertools.chain(*[[i, n//i] for i in range(1, int(n**.5) + 1) if n % i == 0]))
    return a


class Cpu:
    def __init__(self):
        self.registers = [0, 0, 0, 0, 0, 0]

    def execute(self, instruction):
        t = {
            'addr': lambda _a, _b, _c: self.addr(_a, _b, _c),
            'addi': lambda _a, _b, _c: self.addi(_a, _b, _c),
            'mulr': lambda _a, _b, _c: self.mulr(_a, _b, _c),
            'muli': lambda _a, _b, _c: self.muli(_a, _b, _c),
            'banr': lambda _a, _b, _c: self.banr(_a, _b, _c),
            'bani': lambda _a, _b, _c: self.bani(_a, _b, _c),
            'borr': lambda _a, _b, _c: self.borr(_a, _b, _c),
            'bori': lambda _a, _b, _c: self.bori(_a, _b, _c),
            'setr': lambda _a, _b, _c: self.setr(_a, _b, _c),
            'seti': lambda _a, _b, _c: self.seti(_a, _b, _c),
            'gtir': lambda _a, _b, _c: self.gtir(_a, _b, _c),
            'gtri': lambda _a, _b, _c: self.gtri(_a, _b, _c),
            'gtrr': lambda _a, _b, _c: self.gtrr(_a, _b, _c),
            'eqir': lambda _a, _b, _c: self.eqir(_a, _b, _c),
            'eqri': lambda _a, _b, _c: self.eqri(_a, _b, _c),
            'eqrr': lambda _a, _b, _c: self.eqrr(_a, _b, _c),
        }
        return t[instruction[0]](*instruction[1:])

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]
        return self.registers

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b
        return self.registers

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]
        return self.registers

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b
        return self.registers

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]
        return self.registers

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b
        return self.registers

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]
        return self.registers

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b
        return self.registers

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]
        return self.registers

    def seti(self, a, b, c):
        self.registers[c] = a
        return self.registers

    def gtir(self, a, b, c):
        self.registers[c] = int(a > self.registers[b])
        return self.registers

    def gtri(self, a, b, c):
        self.registers[c] = int(self.registers[a] > b)
        return self.registers

    def gtrr(self, a, b, c):
        self.registers[c] = int(self.registers[a] > self.registers[b])
        return self.registers

    def eqir(self, a, b, c):
        self.registers[c] = int(a == self.registers[b])
        return self.registers

    def eqri(self, a, b, c):
        self.registers[c] = int(self.registers[a] == b)
        return self.registers

    def eqrr(self, a, b, c):
        self.registers[c] = int(self.registers[a] == self.registers[b])
        return self.registers
