import numpy as np
import heapq as hq


def prim(G):
	n = G.shape[0]
	G[range(n),range(n)] = np.inf
	visited = [False for i in range(n)]
	R = np.zeros((n,n))
	nodes = range(n)
	Heap = []
	for i in range(n):
		hq.heappush(Heap,[G[0][i],0,i])
	visited[0] = True
	nodes.remove(0)
	while nodes:
		weight,node1,node2 = hq.heappop(Heap)
		if not visited[node2]:
			R[node1,node2] = R[node2,node1] = weight
			nodes.remove(node2)
			visited[node2] = True
			for i in range(n):
				if not visited[i]:
					hq.heappush(Heap,[G[node2][i],node2,i])
	return R



