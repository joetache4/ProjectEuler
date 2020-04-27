"""
Consider an equilateral triangle in which straight lines are drawn from each vertex to the middle of the opposite side, such as in the size 1 triangle in the sketch below.

Sixteen triangles of either different shape or size or orientation or location can now be observed in that triangle. Using size 1 triangles as building blocks, larger triangles can be formed, such as the size 2 triangle in the above sketch. One-hundred and four triangles of either different shape or size or orientation or location can now be observed in that size 2 triangle.

It can be observed that the size 2 triangle contains 4 size 1 triangle building blocks. A size 3 triangle would contain 9 size 1 triangle building blocks and a size n triangle would thus contain n2 size 1 triangle building blocks.

If we denote T(n) as the number of triangles present in a triangle of size n, then

T(1) = 16
T(2) = 104

Find T(36).

ans: 343047
"""


"""
Solution Method:
1. Create an index matrix that translates x-y coordinates into an index for adjacency matrices
2. Create 6 adjacency matrices for each of the six directions
3. For each ad. matrix, create edges between every pair of vertices in the same subgraph
4. Remove reflexive edges - edges with the same start and end point
5. Take every permutation of 3 ad. matrices and multiply them together
6. Find the trace of each product and sum the result 
7. Divide by 6 - this is the solution

This method works because the product of adjacency matrices tells you the number of paths from one vertex to another. We multiply permutations of ad. matrices because this ensures we don't count any paths that double-back on themselves. These ad. matrices don't have reflexive edges because we don't want to count "paths" that stay put at a vertex. However, when we finally take the trace of a ad. matrix product, we're counting the number of length-3 paths that start and stop at the same vertex - i.e. triangles. The answer is divided by six because each triangle was counted 6 times - 3 times starting at each vertex and 2 times more for clockwise and counter-clockwise. 
"""

import numpy as np
import scipy.sparse
import sys

# Note: depth is 1-indexed
def main(depth):
	# create index matrix
	print("creating index matrix")
	mat_index, num_vertices = index(depth)
	
	print("creating adjacency matrices")
	h  = mat_h (mat_index, num_vertices)
	v  = mat_v (mat_index, num_vertices)
	d1 = mat_d1(mat_index, num_vertices)
	d2 = mat_d2(mat_index, num_vertices)
	s1 = mat_s1(mat_index, num_vertices)
	s2 = mat_s2(mat_index, num_vertices)
	
	print("finding paths")
	print("|" + " " * 120 + "|")
	print("|", end="")
	m = [v, h, d1, d2, s1, s2]
	tot = 0
	for a in m:
		for b in m:
			if b is a: continue
			for c in m:
				if c is a or c is b: continue
				tot += a.dot(b).dot(c).diagonal().sum()
				print("=", end="")
				sys.stdout.flush()
	print("|")
	print(f"T({depth}) = {tot//6}")

# used to convert x-y coordinates into an index into the adjacency matrix
def index(depth):
	# max width = 4*depth - 1 (depth 1-indexed)
	# even rows = r + 1 (r 0-indexed)
	# odd rows  = 4*r - 1
	# height    = 2*depth + 1
	mat = np.full((2*depth+1, 4*depth+1), -1)
	i = 0
	for r in range(2*depth + 1):
		if r % 2 == 0:
			for c in range(0, 2*r + 1, 2):
				mat[r, c] = i
				i += 1
		else:
			for c in range(2*r + 1):
				mat[r, c] = i
				i += 1
	return (mat, i)

# create an adjacency matrix with only horizontal connections
def mat_h(index, num_vertices):	
	# create adjacency matrix
	mat = np.zeros((num_vertices, num_vertices), dtype = np.uint8)
	for r in range(2, index.shape[0], 2):
		rep = r
		for c in range(rep):
			c = 2*c
			
			i = index[r, c]
			j = index[r, c + 2]
			mat[i, j] = 1
			mat[j, i] = 1
			
	mat = scipy.sparse.coo_matrix(mat, dtype = np.uint32)	
	return connect(mat)

# create an adjacency matrix with only vertical connections
def mat_v(index, num_vertices):	
	# create adjacency matrix
	mat = np.zeros((num_vertices, num_vertices), dtype = np.uint8)
	for r in range(0, index.shape[0] - 2, 2):
		rep = r + 1 # number of times to repeat
		for c in range(rep):
			c = 2*c
		
			i = index[r    , c    ]
			j = index[r + 1, c + 1]			
			mat[i, j] = 1
			mat[j, i] = 1
		
			i = index[r + 2, c + 2]		
			mat[i, j] = 1
			mat[j, i] = 1
			
	mat = scipy.sparse.coo_matrix(mat, dtype = np.uint32)	
	return connect(mat)

# create an adjacency matrix with only diagonal connections (1)
def mat_d1(index, num_vertices):	
	# create adjacency matrix
	mat = np.zeros((num_vertices, num_vertices), dtype = np.uint8)
	for r in range(0, index.shape[0] - 2, 2):
		rep = r // 2 + 1
		for c in range(rep):
			c = 4*c
			
			i = index[r    , c]
			j = index[r + 1, c]
			mat[i, j] = 1
			mat[j, i] = 1
			i = index[r + 2, c]
			mat[i, j] = 1
			mat[j, i] = 1
			
	mat = scipy.sparse.coo_matrix(mat, dtype = np.uint32)	
	return connect(mat)

# create an adjacency matrix with only diagonal connections (2)
def mat_d2(index, num_vertices):	
	# create adjacency matrix
	mat = np.zeros((num_vertices, num_vertices), dtype = np.uint8)
	for r in range(0, index.shape[0] - 2, 2):
		rep = r // 2 + 1
		for c in range(rep):
			c = 4*c
			
			i = index[r    , c    ]
			j = index[r + 1, c + 2]
			mat[i, j] = 1
			mat[j, i] = 1
			i = index[r + 2, c + 4]
			mat[i, j] = 1
			mat[j, i] = 1
			
	mat = scipy.sparse.coo_matrix(mat, dtype = np.uint32)	
	return connect(mat)

# create an adjacency matrix with only shallow diagonal connections (1)
def mat_s1(index, num_vertices):	
	# create adjacency matrix
	mat = np.zeros((num_vertices, num_vertices), dtype = np.uint8)
	for r in range(1, index.shape[0] - 1, 2):
		# do initial half-pattern
		i = index[r + 1, 0]
		j = index[r    , 1]			
		mat[i, j] = 1
		mat[j, i] = 1
		i = index[r    , 2]		
		mat[i, j] = 1
		mat[j, i] = 1
		
		rep = (r - 1) // 2 # number of times to repeat a full-pattern
		
		for c in range(rep):
			c = 4*c + 2
		
			i = index[r    , c    ]
			j = index[r    , c + 1]			
			mat[i, j] = 1
			mat[j, i] = 1		
			i = index[r - 1, c + 2]		
			mat[i, j] = 1
			mat[j, i] = 1
		
			i = index[r + 1, c + 2]
			j = index[r    , c + 3]			
			mat[i, j] = 1
			mat[j, i] = 1		
			i = index[r    , c + 4]		
			mat[i, j] = 1
			mat[j, i] = 1
			
	mat = scipy.sparse.coo_matrix(mat, dtype = np.uint32)	
	return connect(mat)

# create an adjacency matrix with only shallow diagonal connections (2)
def mat_s2(index, num_vertices):	
	# create adjacency matrix
	mat = np.zeros((num_vertices, num_vertices), dtype = np.uint8)
	for r in range(1, index.shape[0] - 1, 2):
		# do initial half-pattern
		i = index[r, 0]
		j = index[r, 1]			
		mat[i, j] = 1
		mat[j, i] = 1
		i = index[r + 1, 4]
		mat[i, j] = 1
		mat[j, i] = 1
		
		rep = (r - 1) // 2 # number of times to repeat a full-pattern
		
		for c in range(rep):
			c = 4*c
		
			i = index[r - 1, c    ]
			j = index[r    , c + 3]			
			mat[i, j] = 1
			mat[j, i] = 1		
			i = index[r    , c + 4]		
			mat[i, j] = 1
			mat[j, i] = 1
		
			j = index[r    , c + 5]			
			mat[i, j] = 1
			mat[j, i] = 1		
			i = index[r + 1, c + 8]		
			mat[i, j] = 1
			mat[j, i] = 1
			
	mat = scipy.sparse.coo_matrix(mat, dtype = np.uint32)
	return connect(mat)

# take an initial adjacency matrix and create edges between 
# all pairs of vertices that come from the same subgraph - 
# do not create reflexive edges 
def connect(a):
	while True:
		tmp = normalize(a + a.dot(a))
		if (a != tmp).nnz > 0:
			a = tmp
		else:
			return zero_diagonal(a)

# replace all nonzero entries with ones in a sparse matrix
def normalize(a):
	#return np.ceil(a.power(-0.5))
	nnz_inds = a.nonzero()
	keep = np.where(a.data != 0)[0]
	n_keep = len(keep)
	b = scipy.sparse.coo_matrix(
		(np.ones(n_keep), (nnz_inds[0][keep], nnz_inds[1][keep])), 
		shape = a.shape,
		dtype = np.uint32)
	return b

# zero-out the diagonal elements of a sparse matrix
def zero_diagonal(a):
	return a - scipy.sparse.dia_matrix(
		(a.diagonal()[scipy.newaxis, :], [0]), 
		shape = a.shape,
		dtype = np.uint32)

#main(1)
#main(2)
main(36)