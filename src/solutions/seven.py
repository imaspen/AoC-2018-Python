from collections import defaultdict

__author__ = "Aspen Thompson"


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
    pass
