def manhatan_tourist_problem(n, m, down, right):
    s = [[0] * (m + 1) for i in range(n + 1)]
    for i in range(1, n + 1):
        s[i][0] = s[i - 1][0] + down[i - 1][0]
    for j in range(1, m + 1):
        s[0][j] = s[0][j - 1] + right[0][j - 1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s[i][j] = max(s[i - 1][j] + down[i - 1][j], s[i][j - 1] + right[i][j - 1])
    return s[n][m]


if __name__ == "__main__":
    with open('Manhattan_tourist.txt') as f:
        line = f.readline().strip().split()
        n = int(line[0])
        m = int(line[1])
        down = []
        for i in range(n):
            line = f.readline().strip().split()
            down.append([int(i) for i in line])
        f.readline()
        right = []
        for i in range(n + 1):
            line = f.readline().strip().split()
            right.append([int(i) for i in line])
    print(manhatan_tourist_problem(n, m, down, right))
