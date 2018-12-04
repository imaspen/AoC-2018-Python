from collections import defaultdict

__author__ = "Aspen Thompson"


def part_one(lines):
    lines.sort()
    guards = defaultdict(Guard)
    current_id = 0
    for line in lines:
        parts = line.split()
        if parts[2] == "Guard":
            current_id = parts[3][1:]
        else:
            guards[current_id].add_log(line)

    sleepy_id = max(guards, key=lambda guard: guards[guard].sleep_duration)
    return max(guards[sleepy_id].sleep_minutes, key=guards[sleepy_id].sleep_minutes.get) * int(sleepy_id)


class Guard:
    def __init__(self):
        self.log_lines = []

    def add_log(self, line):
        self.log_lines.append(line)

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
    def sleep_duration(self):
        return sum(self.sleep_minutes.values())
