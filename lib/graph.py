# Dijkstra's Min Path Algorithm
'''
from queue import PriorityQueue

def Dijkstra(vertices, source, target):

      create vertex set Q

      for each vertex v in Graph:
          dist[v] ← INFINITY
          prev[v] ← UNDEFINED
          add v to Q
      dist[source] ← 0

      while Q is not empty:
          u ← vertex in Q with min dist[u]

          remove u from Q

          for each neighbor v of u:           // only v that are still in Q
              alt ← dist[u] + length(u, v)
              if alt < dist[v]:
                  dist[v] ← alt
                  prev[v] ← u

      return dist[], prev[]
'''



# Kruskal's Algorithm for Minimum Spanning Tree
# edges: edge matrix
def min_spanning_tree(edges):
	def top_parent(parents, v):
		while True:
			p = parents[v]
			if p == v:
				break
			v = p
		return p

	def fully_connected(parents):
		return all(( p == 0 or v != p for v,p in parents.items() ))

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