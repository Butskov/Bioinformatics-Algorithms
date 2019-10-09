def breakpoints(P):
    adj = 0
    for i in range(len(P) - 1):
        if P[i + 1] - P[i] == 1:
            adj += 1
    if P[0] == 1:
        adj += 1
    if P[-1] == len(P):
        adj += 1
    return len(P) + 1 - adj

if __name__ == '__main__':
    with open('NumberOfBreakpoints.txt') as f:
        P = f.readline().strip()
    P = P[1:-1].split()
    P = [int(i) for i in P]
    print(P)
    print(breakpoints(P))