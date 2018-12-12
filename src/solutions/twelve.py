__author__ = "Aspen Thompson"
__date__ = "2018-12-12"


def get_state(string):
    state = dict()
    for i in range(-2000, 2000):
        state[i] = 0
    for i, char in enumerate(string):
        state[i] = 0 if char == '.' else 1
    return state


def get_rules(rules):
    def get_rule(string):
        return [0 if char == '.' else 1 for char in string]
    rules = [rule.split(" => ") for rule in rules]
    return [(tuple(get_rule(rule[0])), get_rule(rule[1])[0])
            for rule in rules]


def next_state(state, rules):
    next_generation = {-2000: 0, -1999: 0, 1998: 0, 1999: 0}
    for i in range(-1998, 1998):
        part = tuple([state[i + j] for j in range(-2, 3)])
        next_generation[i] = 0
        for rule in rules:
            if rule[0] == part:
                next_generation[i] = rule[1]
                break
    return next_generation


def get_total(state):
    total = 0
    for key in state.keys():
        total += key * state[key]
    return total


def part_one(lines):
    state = get_state(lines[0][15:])
    rules = get_rules(lines[2:])
    for run in range(0, 20):
        state = next_state(state, rules)
    return get_total(state)


def part_two(lines):
    state = get_state(lines[0][15:])
    rules = get_rules(lines[2:])
    last_total = 0
    diff = 0
    for run in range(0, 200):
        state = next_state(state, rules)
        total = get_total(state)
        diff = total - last_total
        last_total = total
    return last_total + (50000000000 - 200) * diff
