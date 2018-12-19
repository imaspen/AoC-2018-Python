import itertools
from collections import defaultdict

__author__ = "Aspen Thomspon"
__date__ = "2018-12-16"


def get_tests(lines):
    instructions = []
    i = 3
    while True:
        if lines[i] == "":
            temp = lines[i - 3: i]
            temp[0] = temp[0][9:-1].split(", ")
            temp[0] = [int(i) for i in temp[0]]
            temp[1] = temp[1].split(" ")
            temp[1] = [int(i) for i in temp[1]]
            temp[2] = temp[2][9:-1].split(", ")
            temp[2] = [int(i) for i in temp[2]]
            instructions.append(temp)
            i += 4
        else:
            return instructions


def get_program(lines):
    ret = []
    for line in lines[3162:]:
        ret.append([int(i) for i in line.split(" ")])
    return ret


def part_one(lines):
    tests = [
        lambda _a, _b, _c: Cpu(*_a).addr(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).addi(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).mulr(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).muli(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).banr(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).bani(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).borr(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).bori(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).setr(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).seti(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).gtir(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).gtri(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).gtrr(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).eqir(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).eqri(*_b[1:]) == _c,
        lambda _a, _b, _c: Cpu(*_a).eqrr(*_b[1:]) == _c,
    ]
    instructions = get_tests(lines)
    count = 0
    for instruction in instructions:
        passed = sum([int(test(instruction[0], instruction[1], instruction[
            2])) for test in tests])
        count += int(passed >= 3)
    return count


def part_two(lines):
    def get_translator(_lines):
        tests = [
            lambda _a, _b, _c: Cpu(*_a).addr(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).addi(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).mulr(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).muli(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).banr(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).bani(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).borr(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).bori(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).setr(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).seti(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).gtir(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).gtri(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).gtrr(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).eqir(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).eqri(*_b[1:]) == _c,
            lambda _a, _b, _c: Cpu(*_a).eqrr(*_b[1:]) == _c,
        ]
        instructions = get_tests(_lines)
        count = 0
        translator = [[True for i in range(16)] for i in range(16)]
        for instruction in instructions:
            passed = [test(instruction[0], instruction[1], instruction[
                2]) for test in tests]
            translator[instruction[1][0]] = [
                item[0] and item[1] for item in zip(
                    translator[instruction[1][0]], passed
                )
            ]
        specifics = defaultdict(int)
        while sum(itertools.chain(*translator)) > 0:
            j = None
            for i in range(len(translator)):
                rule = translator[i]
                if sum(rule) == 1:
                    j = rule.index(True)
                    specifics[i] = j
            for i in range(len(translator)):
                translator[i][j] = False
        return specifics
    rules = get_translator(lines)
    cpu = Cpu(0, 0, 0, 0)
    instructions = [
        cpu.addr,
        cpu.addi,
        cpu.mulr,
        cpu.muli,
        cpu.banr,
        cpu.bani,
        cpu.borr,
        cpu.bori,
        cpu.setr,
        cpu.seti,
        cpu.gtir,
        cpu.gtri,
        cpu.gtrr,
        cpu.eqir,
        cpu.eqri,
        cpu.eqrr
    ]
    program = get_program(lines)
    for instruction in program:
        instructions[rules[instruction[0]]](*instruction[1:])
    return cpu.registers[0]


class Cpu:
    def __init__(self, a, b, c, d):
        self.registers = [a, b, c, d]

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
