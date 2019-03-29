def string_spelled_by_gapped_patterns(k, d, patterns):
    dict = debrujin_graph_from_kmers(patterns)
    path = eulerian_path_problem(dict)
    kmers_path = []
    for i in range(len(path) - 1):
        kmers_path.append((path[i][0] + path[i+1][0][-1], path[i][1] + path[i+1][1][-1]))

    prefix_kmers = [kmer[0] for kmer in kmers_path]
    suffix_kmers = [kmer[1] for kmer in kmers_path]

    prefix_string = ''.join([km[0] for km in prefix_kmers[:-1]] + [prefix_kmers[-1]])
    suffix_string = ''.join([km[0] for km in suffix_kmers[:-1]] + [suffix_kmers[-1]])
    ind_overlap = k+d
    if prefix_string[ind_overlap:] == suffix_string[:-ind_overlap]:
        return prefix_string[:ind_overlap] + suffix_string


def debrujin_graph_from_kmers(patterns):
    kmers = []
    for pattern in patterns:
        kmers = kmers+suffix_composition(len(pattern), pattern, uniq=True)
    kmers = set(kmers)
    dict = {}
    for kmer1 in kmers:
        dict[kmer1] = []
    for kmer in patterns:
        dict[prefix(kmer)].append(suffix(kmer))
    return dict


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
    data = "".join(open('string_spelled_by_gapped_patterns.txt')).split()
    #print(data)
    print(string_spelled_by_gapped_patterns(int(data[0]), int(data[1]), data[2:]))