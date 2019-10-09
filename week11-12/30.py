import numpy as np


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
        if orig % 2 == 0:
            closing = orig - 1
        else:
            closing = orig + 1
        p = []
        i = 0
        while True:
            if orig % 2 == 0:
                p.append(orig // 2)
            else:
                p.append(-(orig + 1) // 2)
            dest = adj[orig - 1] + 1
            i = i + 1
            if (i > 100):

                return
            visited.append(dest)
            if dest == closing:
                genome.append(p)
                break
            if (dest % 2 == 0):
                orig = dest - 1
            else:
                orig = dest + 1
            assert orig > 0
            visited.append(orig)
    return genome


def format_sequence(s):
    fs = []
    for i in s:
        str_p = permutation_list_to_str(i)
        fs.append(str_p)
    return fs


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




if __name__ == '__main__':
    with open('2BreakOnGenome.txt') as f:
        genome = [list(map(int, f.readline().strip()[1:-1].split(' ')))]
        [i, j, k, l] = list(map(int, f.readline().strip().split(', ')))
    genome = two_break_on_genome(genome, i, j, k, l)
    print(''.join(format_sequence(genome)))
