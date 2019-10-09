def hamming_distance(str1, str2, d):

    counter = 0
    for s1, s2 in zip(str1, str2):
        if s1 != s2:
            counter += 1
        if counter > d:
            return 0
    return 1


def make_word(num, k):
    newNum = ''
    while num > 0:
        newNum = str(num % 4) + newNum
        num //= 4
    newNum = "0"*(k - len(newNum)) + newNum
    return newNum


def find_frequent(string, k,d):
    words = []
    result = []

    for i in range(len(string) - k + 1):
        words.append(string[i: i + k])

    mmax = 0
    for i in range(4**k - 1):
        # if (i % 2000) == 0:
        #     print('.', end='')
        testword = make_word(i, k)
        frequenti = 0
        for c in words:
            if hamming_distance(testword, c, d):
                frequenti += 1

        if mmax < frequenti:
            mmax = frequenti
            result = [testword]
        elif mmax == frequenti:
            result.append(testword)

    str_result = []
    for w in result:
        sstr = ""
        for c in w:
            if (c == "0"):
                sstr += "A"
            elif (c == "1"):
                sstr += "C"
            elif (c == "2"):
                sstr += "T"
            elif (c == "3"):
                sstr += "G"
        str_result.append(sstr)
    return str_result

data ="".join(open('frequent_words_mismatch.txt')).split()

data_num = []
for c in data[0]:
    if (c == "A"):
        data_num.append("0")
    elif (c == "C"):
        data_num.append("1")
    elif (c == "T"):
        data_num.append("2")
    elif (c == "G"):
        data_num.append("3")
data[0] = data_num
print(*find_frequent(data[0], int(data[1]), int(data[2])))