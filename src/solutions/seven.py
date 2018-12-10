from collections import defaultdict

__author__ = "Aspen Thompson"
__date__ = "2018-12-07"


def get_rules(rules):
    rule_dict = defaultdict(set)
    for rule in rules:
        rule = rule.split(" must be finished before step ")
        rule_dict[rule[0][-1:]]
        rule_dict[rule[1][:1]].add(rule[0][-1:])
    return rule_dict


def get_ready(rules, completed):
    ready = set()
    for rule in rules:
        if rules[rule].issubset(completed):
            ready.add(rule)
    return ready


def part_one(rules):
    rules = get_rules(rules)
    completed = []
    while True:
        ready = get_ready(rules, set(completed))
        next_rule = sorted(ready)[0]
        rules.pop(next_rule)
        completed.append(next_rule)
        if len(rules) == 0:
            break
    return ''.join(completed)


def part_two(rules):
    rules = get_rules(rules)
    total_rules = len(rules)
    completed = set()
    num_workers = 5
    workers = set()
    seconds = -1

    while len(completed) < total_rules:
        remaining = set()
        for worker in workers:
            worker.time -= 1
            if worker.time == 0:
                completed.add(worker.job)
            else:
                remaining.add(worker)
        workers = remaining
        ready = sorted(get_ready(rules, completed))
        while len(workers) < num_workers and len(ready) > 0:
            next_job = ready.pop(0)
            workers.add(Worker(next_job))
            rules.pop(next_job)
        seconds += 1
    return seconds


class Worker:
    def __init__(self, job):
        self.job = job
        self.time = ord(job) - 4

    def __str__(self):
        return "Worker(job={}, time={})".format(self.job, self.time)
