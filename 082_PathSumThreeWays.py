"""
NOTE: This problem is a more challenging version of Problem 81.

The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the left column and finishing in any cell in the right column, and only moving up, down, and right, is indicated in red and bold; the sum is equal to 994.

Find the minimal path sum from the left column to the right column in matrix.txt (right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.

ans: 260324
"""

from _data.p082 import get_data

m = get_data() # list of rows

test_m = [[131,673,234,103,18],[201,96,342,965,150],[630,803,746,422,111],[537,699,497,121,956],[805,732,524,37,331]]

# return the column on a matrix m given as a list of row lists
def col(m, col):
	c = []
	for row in range(len(m)):
		c.append(m[row][col])
	return c

#assert col(test_m, 0) == [131,201,630,537,805]
#assert col(test_m, 4) == [18,150,111,956,331]

# return the cumulative sum of the entries on the right
# (largest on left)
def cumsum(s):
	cs = s.copy()
	for i in range(len(cs)-2, -1, -1):
		cs[i] = cs[i] + cs[i+1]
	return cs

#a = [1,2,3,4,5]
#assert cumsum(a) == [15,14,12,9,5]
#assert a != [15,14,12,9,5]

# given the cumulative sum of a list, return the sum of entries 
# from start index to end index
def segment_sum(col_cumsum, start, end):
	if end < start:
		start, end = end, start
	ss = col_cumsum[start]
	if end + 1 < len(col_cumsum):
		ss -= col_cumsum[end + 1]
	return ss

#assert segment_sum(cumsum([1,2,3,4,5]), 0, 4) == 15
#assert segment_sum(cumsum([1,2,3,4,5]), 4, 1) == 14
#assert segment_sum(cumsum([1,2,3,4,5]), 1, 2) == 5
#assert segment_sum(cumsum([1,2,3,4,5]), 3, 3) == 4

def main(m):
	#path_sum = cumsum(col(m, n-1))
	n = len(m)
	path_sum = col(m, n-1)

	for c in range(n-2, -1, -1):
		cum = cumsum(col(m, c))
		path_sum = [min(segment_sum(cum, r, r2) + path_sum[r2] for r2 in range(n)) for r in range(n)]

	#return path_sum[0]
	return min(path_sum)

assert main(test_m) == 994

print(main(m))
