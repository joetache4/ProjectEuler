"""
Harder version of problem 18

ans: 7273
"""

from _data.p067 import get_data

def max_pathsum(tri):
	depth = len(tri)
	for level in range(depth - 2, -1, -1):
		for index in range(len(tri[level])):
			tri[level][index] += max(tri[level+1][index], tri[level+1][index+1])
	return tri[0][0]
	
print(max_pathsum(get_data()))