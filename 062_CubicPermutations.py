"""
The cube, 41063625 (3453), can be permuted to produce two other cubes: 56623104 (3843) and 66430125 (4053). In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.


ans: 127035954683
"""

import math

n_len = 1
while True:

	map = {} # sorted digits -> [a^3, b^3, ...]
	ans = []
	
	lo = math.ceil(10**((n_len-1)/3))
	hi = math.ceil(10**(n_len/3) - 1)
	for n in range(lo, hi):
		cube = n**3
		key = "".join(sorted(( d for d in str(cube) )))
		if key not in map:
			map[key] = []
		map[key].append(cube)
	
	for key in map:
		if len(map[key]) == 5:
			ans.append(map[key][0])
	
	if len(ans) > 0:
		break
	
	n_len += 1

print(min(ans))