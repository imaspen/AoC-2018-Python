__author__ = "Aspen Thomspon"
__date__ = "2018-12-21"


def get_program(lines):
    return [[line.split(" ")[0], *[int(i) for i in line.split(" ")[1:]]] for
            line in lines]


def part_one():
    r2 = 0
    r1 = r2 | 65536
    r2 = 1250634
    while True:
        r4 = r1 & 255
        r2 += r4
        r2 &= 16777215
        r2 *= 65899
        r2 &= 16777215
        if 256 <= r1:
            r4 = 0
            while True:
                r3 = r4 + 1
                r3 *= 256
                if r3 <= r1:
                    r4 += 1
                else:
                    break
            r1 = r4
        else:
            break
    return r2


def part_two():
    seen_l = []
    seen = set()
    r2 = 0
    while True:
        r1 = r2 | 65536
        r2 = 1250634
        while True:
            r4 = r1 & 255
            r2 += r4
            r2 &= 16777215
            r2 *= 65899
            r2 &= 16777215
            if 256 <= r1:
                r4 = 0
                while True:
                    r3 = r4 + 1
                    r3 *= 256
                    if r3 <= r1:
                        r4 += 1
                    else:
                        break
                r1 = r4
            else:
                break
        if r2 in seen:
            return seen_l[-1]
        else:
            if len(seen) % 100 == 0:
                print(len(seen), len(seen_l), r2)
            seen.add(r2)
            seen_l.append(r2)
