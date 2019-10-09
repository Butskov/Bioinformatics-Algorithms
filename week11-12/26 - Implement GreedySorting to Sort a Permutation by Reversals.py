from operator import neg


def GreedySorting(P):

	permSeq = []

	kInd = lambda p, k: map(abs, p).index(k)

	kSort = lambda p, i, j: p[:i] + map(neg, p[i:j+1][::-1]) + p[j+1:]

	i = 0
	while i < len(P):
		if P[i] == i+1:
			i += 1
		else:
			P = kSort(P, i, kInd(P, i+1))
			permSeq.append(P)

	return permSeq

'''Input/Output'''
if __name__ == "__main__":
	with open('GreedySorting.txt') as infile:
		p = map(int, infile.read().strip().lstrip('(').rstrip(')').split())
		print(p)
		revList = GreedySorting(p)
		revList = ['('+' '.join([['', '+'][element > 0] + str(element) for element in permutation])+')' for permutation in revList]
		print('\n'.join(revList))


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