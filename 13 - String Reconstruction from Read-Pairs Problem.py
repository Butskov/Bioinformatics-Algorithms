def string_reconstruction_from_read_pairs(patterns, d):
    return genome_path_problem(eulerian_cycle_problem(debruijn_from_read_pairs(patterns)), d)


# def genome_path_problem(kmers, apppend_last=True):
#     genome = ''
#     kmer_length=len(kmers[0])
#     for kmer in kmers:
#         genome += kmer[0]
#     if apppend_last:
#         genome +=  kmer[1:]
#     return genome


def genome_path_problem(path, d):
    text = path[0][0]
    for pair in path[1: d + 2]:
        # [0,d+1) because |pair| = k-1
        text += pair[0][-1]

    text += path[0][1]
    for pair in path[1:]:
        text += pair[1][-1]

    return text


def eulerian_cycle_problem(dict):
    stack = []
    random_vertex = sorted(dict.keys())[0]
    stack.append(random_vertex)
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


def paired_prefix(pair):
    return (pair[0][:-1], pair[1][:-1])

def paired_suffix(pair):
    return (pair[0][1:], pair[1][1:])


def debruijn_from_read_pairs(read_pairs):
    read_pairs = list(read_pairs)

    dict = {}

    for pair in read_pairs:
        pair = pair.split('|')

        suffix = paired_suffix(pair)
        prefix = paired_prefix(pair)

        if prefix in dict.keys():
            dict[prefix].append(suffix)
        else:
            dict[prefix] = [suffix]

    return dict

if __name__ == "__main__":
    data = "".join(open('string_reconstruction_from_read_pairs.txt')).split()
    #print(data)
    print(string_reconstruction_from_read_pairs(data[2:], int(data[1])))
