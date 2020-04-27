"""
The following undirected network consists of seven vertices and twelve edges with a total weight of 243.

The same network can be represented by the matrix below.
	A	B	C	D	E	F	G
A	-	16	12	21	-	-	-
B	16	-	-	17	20	-	-
C	12	-	-	28	-	31	-
D	21	17	28	-	18	19	23
E	-	20	-	18	-	-	11
F	-	-	31	19	-	-	27
G	-	-	-	23	11	27	-

However, it is possible to optimise the network by removing some edges and still ensure that all points on the network remain connected. The network which achieves the maximum saving is shown below. It has a weight of 93, representing a saving of 243 − 93 = 150 from the original network.

Using network.txt (right click and 'Save Link/Target As...'), a 6K text file containing a network with forty vertices, and given in matrix form, find the maximum saving which can be achieved by removing redundant edges whilst ensuring that the network remains connected.

ans: 259679
"""
from queue import PriorityQueue

from _data.p107 import get_data

edges = get_data()

# test
'''
edges = [[-1, 16, 12, 21, -1, -1, -1,],
		[16, -1, -1, 17, 20, -1, -1,],
		[12, -1, -1, 28, -1, 31, -1,],
		[21, 17, 28, -1, 18, 19, 23,],
		[-1, 20, -1, 18, -1, -1, 11,],
		[-1, -1, 31, 19, -1, -1, 27,],
		[-1, -1, -1, 23, 11, 27, -1,]]
'''

def top_parent(parents, v):
	while True:
		p = parents[v]
		if p == v:
			break
		v = p
	return p

def fully_connected(parents): 
	return all(( p == 0 or v != p for v,p in parents.items() ))

# edges = edge matrix
def min_spanning_tree(edges):
	parents  = {v:v for v in range(len(edges))}

	q = PriorityQueue()
	for r in range(len(edges)):
		for c in range(r+1, len(edges[r])):
			if edges[r][c] != -1:
				q.put(( edges[r][c], r, c ))

	# Repeatedly select minimal edges that connect sub-trees
	min_edges = set()
	while not q.empty() and not fully_connected(parents):
		edge_weight, a, b = q.get()
		parent_a = top_parent(parents, a)
		parent_b = top_parent(parents, b)
		if parent_a != parent_b:
			min_edges.add(( edge_weight, a, b ))
			parents[parent_a] = min(parent_a, parent_b)
			parents[parent_b] = parents[parent_a]
	
	return min_edges
	



original_weight = sum(( edges[r][c] for r in range(len(edges)) \
									for c in range(r, len(edges[r])) \
									if edges[r][c] != -1))

weight = sum(( edge[0] for edge in min_spanning_tree(edges) ))

print(f"{original_weight} - {weight} = {original_weight - weight}")
