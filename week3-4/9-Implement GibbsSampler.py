from random import randint, choice
import sys
import numpy

def score(motifs):
    score = 0
    for i in range(len(motifs[0])):
        motif = ''.join([motifs[j][i] for j in range(len(motifs))])
        score += min([hamming_distance(motif, homogeneous*len(motif)) for homogeneous in 'ACGT'])
    return score

def profile_with_pseudocounts(motifs):
    prof = []
    for i in range(len(motifs[0])):
        col = ''.join([motifs[j][i] for j in range(len(motifs))])
        prof.append([float(col.count(nuc)+1)/float(len(col)+4) for nuc in 'ACGT'])
    return prof

def profile_most_probable_kmer(dna, k, prof):
    nuc_loc = {nucleotide:index for index,nucleotide in enumerate('ACGT')}
    max_prob = [-1, None]
    for i in range(len(dna)-k+1):
        current_prob = 1
        for j, nucleotide in enumerate(dna[i:i+k]):
            current_prob *= prof[j][nuc_loc[nucleotide]]
        if current_prob > max_prob[0]:
            max_prob = [current_prob, dna[i:i+k]]

    return max_prob[1]

def motifs_from_profile(profile, dna, k):
    return [profile_most_probable_kmer(seq,k,profile) for seq in dna]

def randomized_motif_search(dna_list,k,t):
    rand_ints = [randint(0,len(dna_list[0])-k) for a in range(t)]
    motifs = [dna_list[i][r:r+k] for i,r in enumerate(rand_ints)]

    # Initialize the best score as a score higher than the highest possible score.
    best_score = [score(motifs), motifs]

    # Iterate motifs.
    while True:
        current_profile = profile_with_pseudocounts(motifs)
        motifs = motifs_from_profile(current_profile, dna_list, k)
        current_score = score(motifs)
        if current_score < best_score[0]:
            best_score = [current_score, motifs]
        else:
            return best_score

def hamming_distance(str1, str2):
    counter = 0
    for s1, s2 in zip(str1, str2):
        if s1 != s2:
            counter += 1
    return counter


def profile_randomized_kmer(dna, k, prof):
    nuc_loc = {nucleotide: index for index, nucleotide in enumerate('ACGT')}
    probs = []
    for i in range(len(dna) - k):
        current_prob = 1.
        for j, nucleotide in enumerate(dna[i:i + k]):
            current_prob *= prof[j][nuc_loc[nucleotide]]
        probs.append(current_prob)

    i = numpy.random.choice(len(probs), p = numpy.array(probs) / numpy.sum(probs))
    return dna[i:i + k]


def gibbs_sampling_motif_search(dna_list, k, t, N, init_motifs=None):
    if init_motifs:
        motifs = init_motifs
    else:
        rand_ints = [randint(0, len(dna_list[0]) - k) for a in range(t)]
        motifs = [dna_list[i][r:r + k] for i, r in enumerate(rand_ints)]

    best_score = [score(motifs), list(motifs)]

    for j in range(N):
        i = randint(0, t - 1)
        current_profile = profile_with_pseudocounts([x for amotif, x in enumerate(motifs) if amotif != i])
        motifs[i] = profile_randomized_kmer(dna_list[i], k, current_profile)
        current_score = score(motifs)
        if current_score < best_score[0]:
            best_score = [current_score, list(motifs)]

    return best_score


if __name__ == '__main__':
    data = "".join(open('gibbs.txt')).split()
    k, t, N = int(data[0]), int(data[1]), int(data[2])
    dna_list = data[3:]
    best_motifs = [k * t, None]
    for repeat in range(20):
        current_motifs = gibbs_sampling_motif_search(dna_list, k, t, N)
        if current_motifs[0] < best_motifs[0]:
            best_motifs = current_motifs
    print('\n'.join(best_motifs[1]))