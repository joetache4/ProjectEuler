"""
Consider the problem of building a wall out of 2×1 and 3×1 bricks (horizontal×vertical dimensions) such that, for extra strength, the gaps between horizontally-adjacent bricks never line up in consecutive layers, i.e. never form a "running crack".

For example, the following 9×3 wall is not acceptable due to the running crack shown in red:

There are eight ways of forming a crack-free 9×3 wall, written W(9,3) = 8.

Calculate W(32,10).


ans: 806844323190414
"""

import numpy as np
import scipy.sparse

m = 32
n = 10

levels = [] # ways to arrange 2- and 3-bricks on a single level
def get_levels(m, level = None):
	last_brick = 0
	if level is None:
		level = []
	else:
		last_brick = level[-1]
	if last_brick in [m-2, m-3]:
		levels.append(level.copy())
	elif last_brick > m-2:
		return
	level.append(last_brick + 2)
	get_levels(m, level)
	level[-1] += 1
	get_levels(m, level)
	level.pop()
get_levels(m)

adj_mat = [] # adjacency matrix
for i in range(len(levels)):
	adj_vec = []
	for j in range(len(levels)):
		if i == j:
			adj_vec.append(0)
		elif all((k not in levels[j] for k in levels[i])):
			adj_vec.append(1)
		else:
			adj_vec.append(0)
	adj_mat.append(adj_vec)

adj_mat = np.matrix(adj_mat, np.uint8)
adj_mat = scipy.sparse.coo_matrix(adj_mat, dtype = np.uint64)

def pow(base, exp):
	if exp == 1:
		return base
	elif exp % 2 == 0:
		tmp = pow(base, exp//2)
		return tmp.dot(tmp)
	else:
		tmp = pow(base, exp - 1)
		return tmp.dot(base)

adj_mat = pow(adj_mat, n - 1)
print(adj_mat.sum(dtype = np.uint64))
