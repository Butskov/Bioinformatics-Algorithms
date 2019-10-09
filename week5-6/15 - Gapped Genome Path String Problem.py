# StringSpelledByGappedPatterns(GappedPatterns, k, d)
#         first_patterns ← the sequence of initial k-mers from GappedPatterns
#         second_patterns ← the sequence of terminal k-mers from GappedPatterns
#         PrefixString ← StringSpelledByGappedPatterns(first_patterns, k)
#         SuffixString ← StringSpelledByGappedPatterns(second_patterns, k)
#         for i = k + d + 1 to |PrefixString|
#             if the i-th symbol in PrefixString does not equal the (i - k - d)-th symbol in SuffixString
#                 return "there is no string spelled by the gapped patterns"
#         return PrefixString concatenated with the last k + d symbols of SuffixString


def string_spelled_by_gapped_patterns(path, k, d):
    first_patterns = [n for n, m in path]
    second_patterns = [m for n, m in path]
    prefix_string = string_spelled_by_patterns(first_patterns, k)
    suffix_string = string_spelled_by_patterns(second_patterns, k)
    for i in range((k + d + 1), len(prefix_string)):
        if prefix_string[i] != suffix_string[i - k - d]:
            return "There is no string spelled by the gapped patterns"
    return prefix_string + suffix_string[-k - d:]


def string_spelled_by_patterns(patterns, k):
    str = patterns[0]
    for i in range(1, len(patterns)):
        str += patterns[i][-1]
    return str


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


def paired_prefix(pair):
    return (pair[0][:-1], pair[1][:-1])


def paired_suffix(pair):
    return (pair[0][1:], pair[1][1:])


def eulerian_path_problem(dict):
    stack = []
    balanced_count = get_balance_count(dict)
    stack.append([k for k, v in balanced_count.items() if v == -1][0])
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
    for i in range(len(text) + 1 - k):
        kmers.append(text[i:i + k - 1])
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
    # print(data)
    print(string_spelled_by_gapped_patterns(eulerian_path_problem(debruijn_from_read_pairs(data[2:])), int(data[0]),
                                            int(data[1])))
