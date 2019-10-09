import numpy as np


def two_break_sorting(P, Q):
    red = colored_edges(Q)
    path = [P]
    while two_break_distance(P, Q) > 0:
        cycles = colored_edges_cycles(colored_edges(P), red)
        for i in cycles:
            if len(i) >= 4:
                P = two_break_on_genome(P, i[0], i[1], i[3], i[2])
                path.append(P)
                break
    return path


def two_break_on_genome(genome, i, j, k, l):
    g = colored_edges(genome)
    g = two_break_on_genome_graph(g, i, j, k, l)
    genome = graph_to_genome(g)
    return genome


def two_break_on_genome_graph(g, i, j, k, l):
    rem = ((i, j), (j, i), (k, l), (l, k))
    bg = [t for t in g if t not in rem]
    bg.append((i, k))
    bg.append((j, l))
    return bg


def two_break_distance(P, Q):
    blue = colored_edges(P)
    red = colored_edges(Q)
    size = len(blue) + len(red)
    l = colored_edges_cycles(blue, red)
    return size // 2 - len(l)


def permutation_list_to_str(p):
    ps = []
    for i in p:
        if i > 0:
            ps.append('+' + str(i))
        elif i == 0:
            ps.append('0')
        elif i < 0:
            ps.append(str(i))
    return '(' + ' '.join(ps) + ')'


def permutation_str_to_list(str_p):
    p = list(map(int, str_p.strip()[1:-1].split(' ')))
    return p


def format_sequence(s):
    fs = []
    for i in s:
        str_p = permutation_list_to_str(i)
        fs.append(str_p)
    return fs


def chromosome_to_cycle(p):
    nodes = []
    for i in p:
        if i > 0:
            nodes.append(2 * i - 1)
            nodes.append(2 * i)
        else:
            nodes.append(-2 * i)
            nodes.append(-2 * i - 1)
    return nodes


def cycle_to_chromosome(nodes):
    p = []
    for j in range(0, len(nodes) // 2):
        if nodes[2 * j] < nodes[2 * j + 1]:
            s = j + 1
        else:
            s = -(j + 1)
        p.append(s)
    return p


def genome_str_to_list(genome):
    lp = []
    for p in genome.split('(')[1:]:
        p = permutation_str_to_list('(' + p)
        lp.append(p)
    return lp


def colored_edges(genome):
    g = []
    for p in genome:
        s = chromosome_to_cycle(p)
        for j in range(len(s) // 2):
            head = 1 + 2 * j
            tail = (2 + 2 * j) % len(s)
            e = (s[head], s[tail])
            g.append(e)
    return g


def graph_to_genome(g):
    genome = []
    visited = []
    adj = np.zeros(len(g) * 2, dtype=np.int)
    for t in g:
        adj[t[0] - 1] = t[1] - 1
        adj[t[1] - 1] = t[0] - 1

    for t in g:
        orig = t[0]
        if orig in visited:
            continue
        visited.append(orig)
        if (orig % 2 == 0):
            closing = orig - 1
        else:
            closing = orig + 1
        p = []
        i = 0
        while (True):
            if (orig % 2 == 0):
                p.append(orig // 2)
            else:
                p.append(-(orig + 1) // 2)
            dest = adj[orig - 1] + 1
            i = i + 1
            if (i > 100):

                return
            visited.append(dest)
            if (dest == closing):
                genome.append(p)
                break
            if (dest % 2 == 0):
                orig = dest - 1
            else:
                orig = dest + 1
            assert orig > 0
            visited.append(orig)
    return genome


def colored_edges_cycles(blue, red):
    cycles = []
    size = len(blue) + len(red)
    adj = np.zeros(shape=(size, 2), dtype=np.int)
    visiteded = np.zeros(shape=size, dtype=np.bool)
    for e in blue:
        adj[e[0] - 1, 0] = e[1] - 1
        adj[e[1] - 1, 0] = e[0] - 1
    for e in red:
        adj[e[0] - 1, 1] = e[1] - 1
        adj[e[1] - 1, 1] = e[0] - 1

    for node in range(size):
        if not visiteded[node]:
            visiteded[node] = True
            head = node
            cycle = [head + 1]
            color = 0
            while True:
                node = adj[node, color]
                if node == head:
                    cycles.append(cycle)
                    break
                cycle.append(node + 1)
                visiteded[node] = True
                color = (color + 1) % 2
    return cycles


if __name__ == '__main__':
    with open('2BreakSorting.txt') as f:
        P = [list(map(int, f.readline().strip()[1:-1].split(' ')))]
        Q = [list(map(int, f.readline().strip()[1:-1].split(' ')))]
    path = two_break_sorting(P, Q)
    result = ''
    for p in path:
        print(''.join(format_sequence(p)))
