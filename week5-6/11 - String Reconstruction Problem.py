# StringReconstruction(Patterns)
# # dB ← DeBruijn(Patterns)
# # path ← EulerianPath(dB)
# # Text﻿ ← PathToGenome(path)
# # return Text
def string_reconstruction_problem(patterns):
    return genome_path_problem(eulerian_path_problem(debrujin_graph_from_kmers(patterns)))


def debrujin_graph_from_kmers(patterns):
    kmers = []
    for pattern in patterns:
        kmers = kmers + suffix_composition(len(pattern), pattern, uniq=True)
    kmers = set(kmers)
    dict = {}
    for kmer1 in kmers:
        dict[kmer1] = []
    for kmer in patterns:
        dict[prefix(kmer)].append(suffix(kmer))
    return dict


def genome_path_problem(kmers, apppend_last=True):
    genome = ''
    kmer_length = len(kmers[0])
    for kmer in kmers:
        genome += kmer[0]
    if apppend_last:
        genome += kmer[1:]
    return genome

def eulerian_path_problem(dict):
    stack=[]
    balanced_count = get_balance_count(dict)
    stack.append([k for k, v in balanced_count.items() if v==-1][0])
    path = []
    while stack != []:
        u_v = stack[-1]
        try:
            w = dict[u_v][0]
            stack.append(w)
            dict[u_v].remove(w)
        except:
            path.append(stack.pop())
    return path[::-1]


def suffix_composition(k, text, uniq=False):
    kmers = []
    for i in range(len(text)+1-k):
        kmers.append(text[i:i+k-1])
    if uniq:
        return sorted(list(kmers))
    else:
        return sorted(kmers)


def get_balance_count(adj_list):
    balanced_count = dict.fromkeys(adj_list.keys(), 0)
    # Look for nodes balancing
    for node in adj_list.keys():
        for out in adj_list[node]:
            balanced_count[node] -= 1
            try:
                balanced_count[out] += 1
            except:
                balanced_count[out] = 1
    return balanced_count


def suffix(string):
    return string[1:]


def prefix(string):
    return string[0:-1]


if __name__ == "__main__":
    data = "".join(open('StringReconstructionProblem.txt')).split()
    print(string_reconstruction_problem(data[1:]))



