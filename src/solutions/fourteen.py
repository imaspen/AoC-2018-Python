import numpy

__author__ = "Aspen Thompson"
__date__ = "2018-12-14"


def get_next(scores, positions):
    current_scores = (scores[positions[0]], scores[positions[1]],)
    next_score = sum(current_scores)
    if next_score < 10:
        scores.append(next_score)
    else:
        scores.append(1)
        scores.append(next_score % 10)
    positions = ((positions[0] + current_scores[0] + 1) % len(scores),
                 (positions[1] + current_scores[1] + 1) % len(scores),)
    return scores, positions


def part_one(recipes):
    scores = [3, 7]
    positions = (0, 1,)
    for i in range(2, recipes + 10):
        scores, positions = get_next(scores, positions)
    return scores[recipes:recipes + 10]


def part_two(recipe):
    recipe = [int(char) for char in str(recipe)]
    target = -len(recipe)
    scores = [3, 7]
    positions = (0, 1,)
    while True:
        scores, positions = get_next(scores, positions)
        if scores[target:] == recipe:
            return len(scores) - len(recipe)
        elif scores[target - 1:-1] == recipe:
            return len(scores) - len(recipe) - 1

