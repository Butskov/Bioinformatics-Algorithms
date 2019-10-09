# -*- coding: utf-8 -*-

def StringSpelledByPatterns(patterns, k):
	str = patterns[0]
	for i in range(1,len(patterns)):
		str += patterns[i][-1]
	return str

def StringSpelledByGappedPatterns(patterns, k, d):
	FirstPatterns = [u for u,v in patterns]
	SecondPatterns = [v for u,v in patterns]
	PrefixString = StringSpelledByPatterns(FirstPatterns, k)
	SuffixString = StringSpelledByPatterns(SecondPatterns, k)
	for i in range((k+d+1),len(PrefixString)):
		if PrefixString[i] != SuffixString[i-k-d]:
			return "there is no string spelled by the gapped patterns"
	return PrefixString+SuffixString[-k-d:]



def PairedDeBruijnGraph(patterns):
	result = dict()
	for pattern in patterns:
		PrefixPattern = (pattern[0][:-1],pattern[1][:-1])
		SuffixPattern = (pattern[0][1:],pattern[1][1:])
		if PrefixPattern in result:
			result[PrefixPattern].append(SuffixPattern)
		else:
			result[PrefixPattern] = [SuffixPattern]
	return result


def EulerianCycle(graph):
	current_node = list(graph.keys())[0]
	path = []
	# path = [current_node]

	def FormCycle(node):
		# print(node)
		cycle = [node]
		while True:
			# print(node in graph)
			# print(graph[node])
			cycle.append(graph[node].pop())
			# print(cycle)
			if len(graph[node]) == 0:
				del graph[node]
			# print(graph)
			if cycle[-1] in graph:
				node = cycle[-1]
			else:
				break
			# print(node)
		return cycle

	path.extend(FormCycle(current_node))
	while len(graph)>0:
		for i in range(len(path)):
			if path[i] in graph:
				# print(path[i])
				# print(type(path[i]))
				# print(graph[path[i]])
				current_node = path[i]
				cycle = FormCycle(current_node)
				path = path[:i] + cycle +path[i+1:]
				# break
	return path


def EulerianPath(graph):

	def UnbalancedNode(graph):
		# start = []
		outNodes = set(graph.keys())
		inNodes = []
		for node in outNodes:
			inNodes.extend(graph[node])
		inNodes = set(inNodes)
		# pprint(inNodes)
		# pprint(outNodes)
		end = list(inNodes - outNodes)[0]
		outDegree = dict()
		for node in outNodes:
			outDegree[node] = len(graph[node])
		inDegree = dict()
		for node in graph.keys():
			for inNode in graph[node]:
				inDegree.setdefault(inNode,0)
				inDegree[inNode] += 1
		# pprint(outDegree)
		# pprint(inDegree)
		for node in outDegree:
			if node not in inDegree:
				start = node
				break
			if outDegree[node] > inDegree[node]:
				start = node
		return start,end

	start,end = UnbalancedNode(graph)
	if end in graph:
		graph[end].append(start)
	else:
		graph[end] = [start]
	path = EulerianCycle(graph)
	# print(path)
	divide_point = list(filter(lambda i: path[i:i+2] == [end, start], range(len(path)-1)))[0]
	path = path[divide_point+1:] + path[1:divide_point+1]

	return path


if __name__ == '__main__':
	# with open('./data/StringReconstructionFromReadPairs_test.txt') as f:
	# 	k,d = list(map(int,f.readline().strip().split()))
	# 	patterns = f.readlines()
	# patterns = [list(pattern.strip().split('|')) for pattern in patterns]

	patterns = []
	with open('./data/probelmset3.txt') as f:
		for line in f:
			pattern = line.strip().split('|')
			patterns.append([pattern[0][1:],pattern[1][:-1]])
	print(patterns)
	k=3
	d=1

	# print(k)
	# print(d)
	# print(patterns)
	# print(StringSpelledByGappedPatterns(patterns,k,d))
	graph = PairedDeBruijnGraph(patterns)
	path = EulerianPath(graph)
	# print(path)
	# sortPatterns =
	s = StringSpelledByGappedPatterns(path,k,d)
	print(s)