"""
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?

ans: 296962999629 (2969, 6299, 9629) diff = 3330

(observation) Since this arithmetic progression has 3 terms, the difference between terms must be divisible by 2 and 3. Otherwise, one of the terms would be divisible by 2 or 3, and hence not be prime.
"""

from lib.num import *

digits = 4

def main(digits):
	min_num = 10**(digits-1) + 1
	max_num = 10**digits - 1 - 2*6

	for k in range(min_num, max_num+1, 2):
		#print(k)
		if not is_prime(k):
			continue
		min_diff = 6
		max_diff = (max_num + 4 - k) // 2
		#print("  min_diff: {}, max_diff: {}".format(min_diff, max_diff))
		for d in range(min_diff, max_diff+1, 6):
			#print("  + {}".format(d))
			if not (is_prime(k+d) and is_permutation(k, k+d)):
				continue
			if not (is_prime(k+2*d) and is_permutation(k, k+2*d)):
				continue
			if k != 1487:
				return (k, k+d, k+2*d)
	
	return (-1, -1, -1)
				
a, b, c = main(digits)
# check ans
assert is_prime(a)
assert is_prime(b)
assert is_prime(c)
assert a < b and b < c
assert (c - b) == (b - a)
assert a != 1487
# print ans
print(''.join([str(a), str(b), str(c)]))
print((a, b, c))
print("diff = {}".format(b - a))