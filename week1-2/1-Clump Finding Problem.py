import itertools
from collections import Counter

def find_frequent(string, k,t):
    words = []
    frequent = []

    for i in range(len(string)):
        word = "".join(string[i: i + k])

        if len(word) == k:
            words.append(word)

    return Counter(words).most_common()

def clump_finding_problem(string, k, L, t):
    words = []
    for i in range(len(string)):
        strings1 = string[i:i + L]
        if len(strings1) == L:
            words.append(find_frequent(strings1, k, t))

    pattern = list(itertools.chain(*words))
    print(*set([x[0] for x in pattern if x[1] >= t]))


data = "".join(open('rosalind_ba1e.txt')).split()
clump_finding_problem(data[0], int(data[1]), int(data[2]), int(data[3]))
