from collections import defaultdict

__author__ = "Aspen Thompson"


def generate_guards(lines):
    lines.sort()
    guards = defaultdict(Guard)
    current_id = 0
    for line in lines:
        parts = line.split()
        if parts[2] == "Guard":
            current_id = parts[3][1:]
            guards[current_id].id = current_id
        else:
            guards[current_id].add_log(line)
    return guards


def part_one(lines):
    guards = generate_guards(lines)
    sleepy = guards[max(guards, key=lambda guard: guards[guard].sleep_duration)]
    return max(sleepy.sleep_minutes, key=sleepy.sleep_minutes.get) * sleepy.id


def part_two(lines):
    guards = generate_guards(lines)
    sleepy = guards[max(guards, key=lambda guard: guards[guard].sleepiest_minute[1])]
    return sleepy.id * int(sleepy.sleepiest_minute[0])


class Guard:
    def __init__(self):
        self.id = 0
        self.log_lines = []

    def add_log(self, line):
        self.log_lines.append(line)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, val):
        self.__id = int(val)

    @property
    def sleep_times(self):
        def log_minute(line):
            return line.split(" ")[1].split(":")[1][:-1]

        sleep_times = []
        for i in range(len(self.log_lines) // 2):
            sleep_times.append((
                int(log_minute(self.log_lines[i * 2])),
                int(log_minute(self.log_lines[i * 2 + 1])),
            ))
        return sleep_times

    @property
    def sleep_minutes(self):
        minutes = defaultdict(int)
        for sleep_time in self.sleep_times:
            for i in range(sleep_time[0], sleep_time[1]):
                minutes[i] += 1
        return minutes

    @property
    def sleepiest_minute(self):
        if len(self.sleep_minutes) == 0:
            return 0, 0
        minute = max(self.sleep_minutes, key=self.sleep_minutes.get)
        return minute, self.sleep_minutes[minute]

    @property
    def sleep_duration(self):
        return sum(self.sleep_minutes.values())
