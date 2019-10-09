import copy


def greedy_sorting(P):
    approx_reversal_distance = 0
    permutations = []
    for i in range(1, len(P) + 1):
        if P[i - 1] != i and P[i - 1] != -i:
            index = 0
            if i in P:
                index = P.index(i)
            elif -i in P:
                index = P.index(-i)
            tem = P[i - 1:index + 1]
            tem = [-k for k in tem]
            P[i - 1:index + 1] = tem[::-1]
            permutations.append(copy.copy(P))
            approx_reversal_distance += 1
        if P[i - 1] == -i:
            P[i - 1] = i
            permutations.append(copy.copy(P))
            approx_reversal_distance += 1
    return approx_reversal_distance, permutations


if __name__ == '__main__':
    with open('GreedySorting.txt') as f:
        P = f.readline().strip()
    P = P[1:-1].split()
    P = [int(i) for i in P]
    print(P)
    a, permutations = greedy_sorting(P)
    # print(permutations)
    # for i in permutations:
    #     str_p = ['+' + str(pp) if pp > 0 else str(pp) for pp in i]
    #     print('(%s)' % ' '.join(str_p))
