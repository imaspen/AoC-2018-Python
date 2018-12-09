from collections import defaultdict, deque

__author__ = "Aspen Thompson"
__date__ = "2018-12-09"


def part_one(num_players, last_score):
    players = defaultdict(int)
    marbles = deque([0])
    player = 0
    for marble in range(1, last_score + 1):
        if marble % 23 == 0:
            marbles.rotate(7)
            players[player] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(marble)
        player = (player + 1) % num_players
    return max(players.values())
