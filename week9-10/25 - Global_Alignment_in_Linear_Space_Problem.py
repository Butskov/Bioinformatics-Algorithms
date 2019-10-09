def global_alignment(seq1, seq2, score_matrix, penalty):
    len1, len2 = len(seq1), len(seq2)
    s = [[0] * (len2 + 1) for i in range(len1 + 1)]
    backtrack = [[0] * (len2 + 1) for i in range(len1 + 1)]
    for i in range(1, len1 + 1):
        s[i][0] = - i * penalty
    for j in range(1, len2 + 1):
        s[0][j] = - j * penalty
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            score_list = [s[i - 1][j] - penalty, s[i][j - 1] - penalty,
                          s[i - 1][j - 1] + score_matrix[seq1[i - 1], seq2[j - 1]]]
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


def mid_column_score(v, w, score_matrix, penalty):
    s = [[i * j * penalty for i in range(-1, 1)] for j in range(len(v) + 1)]
    s[0][1] = -penalty
    backtrack = [0] * (len(v) + 1)
    for j in range(1, len(w) // 2 + 1):
        for i in range(0, len(v) + 1):
            if i == 0:
                s[i][1] = -j * penalty
            else:
                scores = [s[i - 1][0] + score_matrix[v[i - 1], w[j - 1]], s[i][0] - penalty, s[i - 1][1] - penalty]
                s[i][1] = max(scores)
                backtrack[i] = scores.index(s[i][1])
        if j != len(w) // 2:
            s = [[row[1]] * 2 for row in s]
    return [i[1] for i in s], backtrack


def mid_edge(v, w, score_matrix, penalty):
    source = mid_column_score(v, w, score_matrix, penalty)[0]
    mid_to_sink, backtrack = list(map(lambda l: l[::-1], mid_column_score(v[::-1], w[::-1] + ['', '$'][
        len(w) % 2 == 1 and len(w) > 1], score_matrix, penalty)))
    scores = list(map(sum, zip(source, mid_to_sink)))
    max_mid = max(range(len(scores)), key = lambda i: scores[i])
    if max_mid == len(scores) - 1:
        next_node = (max_mid, len(w) // 2 + 1)
    else:
        next_node = [(max_mid + 1, len(w) // 2 + 1), (max_mid, len(w) // 2 + 1), (max_mid + 1, len(w) // 2), ][
            backtrack[max_mid]]
    return (max_mid, len(w) // 2), next_node


def linear_space_alignment(top, bottom, left, right, score_matrix):
    v = seq1
    w = seq2
    if left == right:
        return [v[top:bottom], '-' * (bottom - top)]
    elif top == bottom:
        return ['-' * (right - left), w[left:right]]
    elif bottom - top == 1 or right - left == 1:
        return global_alignment(v[top:bottom], w[left:right], score_matrix, penalty)[1:]
    else:
        mid_node, next_node = mid_edge(v[top:bottom], w[left:right], score_matrix, penalty)
        mid_node = tuple(map(sum, zip(mid_node, [top, left])))
        next_node = tuple(map(sum, zip(next_node, [top, left])))
        current = [['-', v[mid_node[0] % len(v)]][next_node[0] - mid_node[0]],
                   ['-', w[mid_node[1] % len(w)]][next_node[1] - mid_node[1]]]
        a = linear_space_alignment(top, mid_node[0], left, mid_node[1], score_matrix)
        b = linear_space_alignment(next_node[0], bottom, next_node[1], right, score_matrix)
        return [a[i] + current[i] + b[i] for i in range(2)]


def linear_space_global_alignment(v, w, score_matrix, penalty):
    align1, align2 = linear_space_alignment(0, len(v), 0, len(w), score_matrix)
    p = []
    for i in zip(align1, align2):
        if '-' in i:
            p.append(-penalty)
        else:
            p.append(score_matrix[i])
    score = sum(p)
    return str(score), align1, align2


if __name__ == '__main__':
    with open('linear_space_alignment.txt') as f:
        seq1 = f.readline().strip()
        seq2 = f.readline().strip()
    with open('BLOSUM62.txt') as f1:
        lines = [line.strip().split() for line in f1.readlines()]
        matrix = {(i[0], i[1]): int(i[2]) for i in lines}
    penalty = 5
    alignment = '\n'.join(linear_space_global_alignment(seq1, seq2, matrix, penalty))
    print(alignment)
