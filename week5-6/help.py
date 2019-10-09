from sys import argv
import random
import fileinput
from itertools import product


def Composition(k, text):
    kmers = []
    for i in range(len(text)+1-k):
        kmers.append(text[i:i+k])
    return sorted(kmers)

def PairedComposition(k, d, text):
    paired_reads = []
    for i in range(len(text)+1-k-d-k):
        paired_reads.append((text[i:i+k], text[i+k+d:i+k+d+k]))
    return sorted(paired_reads)

def PairedPrefix(pair):
    return (pair[0][:-1], pair[1][:-1])

def PairedSuffix(pair):
    return (pair[0][1:], pair[1][1:])
    return None


print(PairedSuffix(("GAC", "TCA")))
def SuffixComposition(k, text, uniq=False):
    kmers = []
    for i in range(len(text)+1-k):
        kmers.append(text[i:i+k-1])
    if uniq:
        return sorted(list(kmers))
    else:
        return sorted(kmers)

def GenomePathProblem(kmers, apppend_last=True):
    genome = ""
    kmer_length=len(kmers[0])
    for kmer in kmers:
        genome+=kmer[0]
    if apppend_last:
        genome+=kmer[1:]
    return genome

def Suffix(text):
    return text[1:]

def Prefix(text):
    return text[0:-1]

# Combining this with integer to pattern will be more efficient
def Overlap(patterns):
    kmers=sorted(patterns)
    adj_list = []
    for k1 in kmers:
        for k2 in kmers:
            if Suffix(k1) == Prefix(k2):
                adj_list.append((k1, k2))
    return adj_list

def deBrujin(k, text):
    kmers = SuffixComposition(k, text)
    overl = Overlap(kmers)
    adj_list = {}
    # Inicializo diccionario
    for kmer in kmers:
        adj_list[kmer]=[]
    for i in range(len(text)+1-k):
        adj_list[text[i:i+k-1]].append(text[i+1:i+k])
    return adj_list

def deBrujinGraphFromKmers(kmers_in):
    #print "Initialazing dictionary"
    kmers = []
    for kmer in kmers_in:
        kmers = kmers+SuffixComposition(len(kmer), kmer, uniq=True )
    kmers = set(kmers)
    adj_dict = {}
    for kmer1 in kmers:
        adj_dict[kmer1] = []
    for kmer in kmers_in:
        adj_dict[Prefix(kmer)].append(Suffix(kmer))
    return adj_dict

def EulerianCycleProblem(adj_list):
    # Choose any vertex and push into stack
    stack=[]
    random_vertex = sorted(adj_list.keys())[0]
    #random_vertex = random.sample(adj_list.keys(), 1)[0]
    stack.append(random_vertex)
    # To save the right path
    path = []
    # Stack but fifo xD
    while stack != []:
        # top vertex
        u_v = stack[-1]
        try:
            w = adj_list[u_v][0]
            stack.append(w)
            # Removeadj_list[u][0] from available edges (edge marked)
            adj_list[u_v].remove(w)
        # No edges
        except:
            path.append(stack.pop())
    return path[::-1]

def getBalanceCount(adj_list):
    balanced_count = dict.fromkeys(adj_list.keys(), 0)
    # Look for nodes balancing
    for node in adj_list.keys():
        #  If is in the sum 1 to balance, if out rest 1
        #print node
        for out in adj_list[node]:
            balanced_count[node] -= 1
            # Possibly there is a node with no out edges
            try:
                balanced_count[out] += 1
            except:
                balanced_count[out] = 1
    return balanced_count

def EulerianPathProblem(adj_list):
    # Choose a unbalanced vertex (with out edge) and push into stack
    stack=[]
    balanced_count = getBalanceCount(adj_list)
    stack.append([k for k, v in balanced_count.iteritems() if v==-1][0])
    # To save the right path
    path = []
    # Stack but fifo xD
    while stack != []:
        # top vertex
        u_v = stack[-1]
        try:
            w = adj_list[u_v][0]
            stack.append(w)
            # Removeadj_list[u][0] from available edges (edge marked)
            adj_list[u_v].remove(w)
        # No edges
        except:
            path.append(stack.pop())
    return path[::-1]

def StringReconstructionProblem(kmers):
    return GenomePathProblem(EulerianPathProblem(deBrujinGraphFromKmers(kmers)))


def BinaryStrings(k):
    universe = ["0", "1"]
    kmers = ["".join(el) for el in product(universe, repeat=k)]
    return sorted(kmers)

def kUniversalStringProblem(k):
    #print deBrujinGraphFromKmers(BinaryStrings(k))
    cycle =  EulerianCycleProblem(deBrujinGraphFromKmers(BinaryStrings(k)))
    #print cycle
    genome = ""
    cycle=cycle[:-(k-1)]
    genome=cycle[0][:-1]
    for n in cycle:
        genome+=n[-1]
    return genome