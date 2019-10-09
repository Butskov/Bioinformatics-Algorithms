def find_position(pattern, string, maxerror):
    position = []
    k = len(pattern)
    for i in range(len(string)):
        word = "".join(string[i: i + k])
        if func(word, pattern, maxerror) == 1:
            position.append(i)
    print(*position)


def func(str, pattern, maxerror):
    if (len(str) != len(pattern)):
        return 0
    errorcount = 0
    for i in range(len(str)):
        if (str[i] != pattern[i]):
            errorcount += 1
        if errorcount > maxerror:
            return 0
    return 1

data ="".join(open('approximate_match.txt')).split()
find_position(data[0], data[1], int(data[2]))