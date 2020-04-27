"""
Let T(n) be the number of tours over a 4 × n playing board such that:

    The tour starts in the top left corner.
    The tour consists of moves that are up, down, left, or right one square.
    The tour visits each square exactly once.
    The tour ends in the bottom left corner.

The diagram shows one tour over a 4 × 10 board:

T(10) is 2329. What is T(10**12) modulo 10**8?

ans: 15836928
"""


"""
Solution Method:
1. Catalogue all possible 4x2  path "slices"
2. Encode how the left side connects to the right side in an adjacency matrix
3. Raise adj. matrix to n/2-th power

The following illustrates how a 4x2 slice is encoded as a 4x2 matrix:
1 indicates a path entering or exiting the slice at the square.
2 indicates a "loop back".

The distinction between 1s and 2s stops path "islands" and premature loops from forming.

1s and 2s on the left will connect to 1s and 2s respectively on the right, with the following exceptions.
A 1 and 2 on the left can connect to each other, the remaining 2 can connect to a 1 on the right.
1s can connect on the left if the right has only 0s.

Examples:
00        _      01        ___    10      ___
11  ==  _| |_    12  ==  _|  _    10  ==  _  |
11      _   _    12      _  |_    21      _| |_
00       |_|     01       |___    21      _____

11 and 11 are unique in that these encodings refer to multiple paths:
00     20
00     20
11     11
_____    _   _    _   _    and    _   _    _____
  _       |_|      | |            _| |     ___ 
 | |       _       |_|            ___|     _  |
_| |_    _| |_     ___            _____    _| |_

The adjacency matrix then looks at all ways the left side (given by a column of 4 ints) can connect to the right side (again given by a column of 4 ints):

index: 0 1 2 3 4 5 6 7 8 9
col  : 1 1 0 2 1 1 1 0 0 0
       0 1 0 2 2 1 0 1 1 0
       0 0 1 1 2 2 1 0 1 0
       1 0 1 1 1 2 0 1 0 0

The 9th column is noteworthy in being all 0s. This indicates the last column of the playing board where all paths need to turn around.
"""

import numpy as np

n = 10**12
m = 10**8

adj_matrix = np.matrix([
[3,1,1,1,1,1,0,1],
[1,1,1,0,1,1,1,1],
[1,1,1,1,1,0,1,1],
[1,1,1,1,1,0,1,1],
[2,1,1,1,1,1,0,1],
[1,1,1,0,1,1,1,1],
[0,1,1,0,1,0,1,1],
[0,0,0,0,0,0,0,0]
], np.int64)

def mod_pow(base, exp, mod):
	if exp <= 0:
		raise Exception("exp nonpositive")
	elif exp == 1:
		return base
	elif exp % 2 == 0:
		tmp = mod_pow(base, exp/2, mod)
		return np.mod(np.matmul(tmp, tmp), mod)
	else:
		tmp = mod_pow(base, exp - 1, mod)
		return np.mod(np.matmul(tmp, base), mod)

def main(width, mod = 10000):
	return mod_pow(adj_matrix, width//2, mod)[0,7]		

print(f"T(4) = {main(4)}")
assert main(4)  == 8

print(f"T(10) = {main(10)}")
assert main(10) == 2329

print(f"T({n}) = {main(n, m)}")