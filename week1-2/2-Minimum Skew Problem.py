data = open('minimum_skew.txt', 'r')

string = data.read()
result = []
position = 0
skew = []
for i in string:
    if i == 'C':
        position += -1
    elif i =='G':
        position += 1
    skew.append(position)


minimum = min(skew)
for i in range(len(skew)):
    if skew[i] == minimum:
        result.append(i+1)

print(*result)
