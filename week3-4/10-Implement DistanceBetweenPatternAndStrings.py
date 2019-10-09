def hamming_distance(str1, str2):
    counter = 0
    for s1, s2 in zip(str1, str2):
        if s1 != s2:
            counter += 1
    return counter

def distance_between_pattern_and_strings(pattern, dna):
    k = len(pattern)
    distance = 0
    for string in dna:
        hammingdistance = float("inf")
        for i in range(len(string) - k + 1):
            if hammingdistance > hamming_distance(pattern, string[i:i + k]):
                hammingdistance = hamming_distance(pattern, string[i:i + k])
        distance = distance + hammingdistance
    return distance


if __name__ == "__main__":
    data = "".join(open('distance_between_pattern_and_strings.txt')).split()
    distance = distance_between_pattern_and_strings(data[0], data[1:])
    print(distance)