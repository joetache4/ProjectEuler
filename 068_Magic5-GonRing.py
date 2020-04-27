"""
Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.

Working clockwise, and starting from the group of three with the numerically lowest external node (4,3,2 in this example), each solution can be described uniquely. For example, the above solution can be described by the set: 4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12. There are eight solutions in total.
Total	Solution Set
9	4,2,3; 5,3,1; 6,1,2
9	4,3,2; 6,2,1; 5,1,3
10	2,3,5; 4,5,1; 6,1,3
10	2,5,3; 6,3,1; 4,1,5
11	1,4,6; 3,6,2; 5,2,4
11	1,6,4; 5,4,2; 3,2,6
12	1,5,6; 2,6,4; 3,4,5
12	1,6,5; 3,5,4; 2,4,6

By concatenating each group it is possible to form 9-digit strings; the maximum string for a 3-gon ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form 16- and 17-digit strings. What is the maximum 16-digit string for a "magic" 5-gon ring?


ans: 6531031914842725
"""

# Indices 0-4 are on the outer ring
# Each connect to its +5 index

from lib.num import permutations

# return code integer if valid 16-digit magic ring, otherwise -1
def ring(p):
	# 10 must be in the outer ring for code to be 16 digits
	if all(( p[i] != 10 for i in range(5) )):
		return -1
	# test if consistent sum along lines
	sums = {p[i] + p[i+5] + p[(i+1)%5+5] for i in range(5)}
	if len(sums) > 1:
		return -1	
	# convert to int
	start = min(( (p[i],i) for i in range(5) ))[1]
	code = []
	for i in range(start, start + 5):
		i %= 5
		code.append(p[i])
		code.append(p[i+5])
		code.append(p[(i+1)%5+5])
	return int("".join(( str(x) for x in code )))

print(max(( ring(p) for p in permutations(range(1,11)) )))