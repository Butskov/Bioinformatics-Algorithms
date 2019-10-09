def global_alignment(seq1, seq2, score_matrix, sig):
    len1, len2 = len(seq1), len(seq2)
    s = [[0] * (len2 + 1) for i in range(len1 + 1)]
    backtrack = [[0] * (len2 + 1) for i in range(len1 + 1)]
    for i in range(1, len1 + 1):
        s[i][0] = - i * sig
    for j in range(1, len2 + 1):
        s[0][j] = - j * sig
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            score_list = [s[i - 1][j] - sig, s[i][j - 1] - sig, s[i - 1][j - 1] + score_matrix[seq1[i - 1], seq2[j - 1]]]
            s[i][j] = max(score_list)
            backtrack[i][j] = score_list.index(s[i][j])
    indel_insert = lambda seq, i: seq[:i] + '-' + seq[i:]
    align1, align2 = seq1, seq2
    a, b = len1, len2
    max_score = str(s[a][b])
    while a * b != 0:
        if backtrack[a][b] == 0:
            a -= 1
            align2 = indel_insert(align2, b)
        elif backtrack[a][b] == 1:
            b -= 1
            align1 = indel_insert(align1, a)
        else:
            a -= 1
            b -= 1
    for i in range(a):
        align2 = indel_insert(align2, 0)
    for j in range(b):
        align1 = indel_insert(align1, 0)
    return max_score, align1, align2


if __name__ == '__main__':
    with open('global_alignment.txt') as f:
        seq1 = f.readline().strip()
        seq2 = f.readline().strip()
    with open('BLOSUM62.txt') as f1:
        lines = [line.strip().split() for line in f1.readlines()]
        score_matrix = {(i[0], i[1]): int(i[2]) for i in lines}
    penalty = 5
    alignment = '\n'.join(global_alignment(seq1, seq2, score_matrix, penalty))
    print(alignment)
