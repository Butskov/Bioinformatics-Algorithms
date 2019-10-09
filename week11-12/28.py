from collections import defaultdict
import re


def two_break_dist(P, Q):
    bp_graph = defaultdict(list)
    # print(type(Q))
    for j in P + Q:
        n = len(j)
        for i in range(n):
            bp_graph[j[i]].append(-1 * j[(i + 1) % n])
            bp_graph[-1 * j[(i + 1) % n]].append(j[i])
    counter = 0
    remain = set(bp_graph.keys())

    while remain:
        counter += 1
        queue = {remain.pop()}

        while queue:
            current = queue.pop()
            new = {node for node in bp_graph[current] if node in remain}

            queue |= new
            remain -= new

    return sum(map(len, P)) - counter


if __name__ == '__main__':
    with open('2BreakDistance.txt') as f:
        P, Q = [line.strip().lstrip('(').rstrip(')').split(')(') for line in f]
        # print(P)
        P = [list(map(int, i.split())) for i in P]
        Q = [list(map(int, i.split())) for i in Q]
    answer = two_break_dist(P, Q)
    print(answer)
