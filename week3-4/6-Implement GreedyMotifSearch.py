'''
GREEDYMOTIFSEARCH(Dna, k, t)
        BestMotifs ← motif matrix formed by first k-mers in each string
                      from Dna
        for each k-mer Motif in the first string from Dna
            Motif1 ← Motif
            for i = 2 to t
                form Profile from motifs Motif1, …, Motifi - 1
                Motifi ← Profile-most probable k-mer in the i-th string
                          in Dna
            Motifs ← (Motif1, …, Motift)
            if Score(Motifs) < Score(BestMotifs)
                BestMotifs ← Motifs
        return BestMotifs
'''
def greedy_motif_search(dna, k, t):
    best_motifs = []
    for i in range(t):
        best_motifs.append(dna[i][:k])

    for i in range(len(dna[0]) - k + 1):
        motifs = []
        motifs.append(dna[0][i: i + k])
        for j in range(1, t):
            profile = create_profile(motifs)
            motifs.append(profile_most_probable(dna[j], profile, k))
        if score(best_motifs) > score(motifs):
            best_motifs = motifs
    return best_motifs


def calculate_probablity(profile, string):
    probablity = 1
    for i in range(0, len(string)):
        if string[i] == 'A':
            probablity = probablity * profile[i][0]
        elif string[i] == 'C':
            probablity = probablity * profile[i][1]
        elif string[i] == 'G':
            probablity = probablity * profile[i][2]
        elif string[i] == 'T':
            probablity = probablity * profile[i][3]
    return probablity


def profile_most_probable(dna_string, profile, k):
    best_pattern = dna_string[0:0 + k]
    best_probability = 0
    for i in range(len(dna_string) - k + 1):
        string = dna_string[i:i + k]
        new_probablity = calculate_probablity(profile, string)
        if new_probablity > best_probability:
            best_pattern = string
            best_probability = new_probablity
    return best_pattern


def create_profile(motifs):
    profile =[]
    for i in range(len(motifs[0])):
        count_A, count_C, count_G, count_T = 0, 0, 0, 0
        for motif in motifs:
            if motif[i] == 'A':
                count_A += 1
            elif motif[i] == 'C':
                count_C += 1
            elif motif[i] == 'G':
                count_G += 1
            elif motif[i] == 'T':
                count_T += 1
        profile.append([count_A / len(motifs), count_C / len(motifs), count_G / len(motifs), count_T / len(motifs)])
    return profile


def hamming_distance(str1, str2):
    counter = 0
    for s1, s2 in zip(str1, str2):
        if s1 != s2:
            counter += 1
    return counter


def find_consensus(motifs):
    consensus = ''
    for i in range(len(motifs[0])):
        count_A, count_C, count_G, count_T = 0, 0, 0, 0
        for motif in motifs:
            if motif[i] == 'A':
                count_A += 1
            elif motif[i] == 'C':
                count_C += 1
            elif motif[i] == 'G':
                count_G += 1
            elif motif[i] == 'T':
                count_T += 1
        if count_A >= max(count_C, count_G, count_T):
            consensus += "A"
        elif count_C >= max(count_A, count_G, count_T):
            consensus += "C"
        elif count_G >= max(count_C, count_A, count_T):
            consensus += "G"
        elif count_T >= max(count_C, count_G, count_A):
            consensus += "T"
    return consensus


def score(motifs):
    consensus = find_consensus(motifs)
    score = 0
    for motif in motifs:
        score += hamming_distance(consensus, motif)
    return score


if __name__ == "__main__":
    data = "".join(open('greedy_motif_search.txt')).split()
    print(*greedy_motif_search(data[2: ], int(data[0]), int(data[1])))

