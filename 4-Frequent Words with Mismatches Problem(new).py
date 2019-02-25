def hamming_distance(str1, str2):

    counter = 0
    for s1, s2 in zip(str1, str2):
        if s1 != s2:
            counter += 1
    return counter


def neighbors(pattern, d):
    if d == 0:
        return pattern
    if len(pattern) == 1:
        return ["A", "C", "G", "T"]
    neighbor= []
    suffixneighbors = neighbors(pattern[1:], d)
    for text in suffixneighbors:
        if hamming_distance(pattern[1:], text) < d:
            for x in ["A", "C", "G", "T"]:
                neighbor.append(x + text)
        else:
            neighbor.append(pattern[0] + text)

    return neighbor


def find_frequent(string, k, d):
    words = []
    neighborhood = set()
    result = []

    for i in range(len(string) - k + 1):
        words.append(string[i: i + k])


    for word in words:
        neighborhood.update(set(neighbors(word, d)))

    mmax = 0
    for i in neighborhood:
        frequenti = 0
        for c in words:
            if hamming_distance(i, c) <= d:
                frequenti += 1

        if mmax < frequenti:
            mmax = frequenti
            result = [i]
        elif mmax == frequenti:
            result.append(i)


    return result

data = "".join(open('frequent_words_mismatch.txt')).split()
print(*find_frequent(data[0], int(data[1]), int(data[2])))