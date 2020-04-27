"""
There are several ways to write the number 1/2 as a sum of inverse squares using distinct integers.

For instance, the numbers {2,3,4,5,7,12,15,20,28,35} can be used:

In fact, only using integers between 2 and 45 inclusive, there are exactly three ways to do it, the remaining two being: {2,3,4,6,7,9,10,20,28,35,36,45} and {2,3,4,6,7,9,12,15,28,30,35,36,45}.

How many ways are there to write the number 1/2 as a sum of inverse squares using distinct integers between 2 and 80 inclusive?


ans: 301
"""

import math
from functools import reduce
from lib.num import factor, lcm, binary_search, get_primes
from lib.list import subsets


# Initial observations:
# primes 41 and above aren't feasible (seen by multiplying lcm, taking mod 41^2 and higher)
# 2 is a necessary term (else remainder is not enough), just subtract it from the target

# let P = prod(2 to 80)^2
# 1/2             = 1/(2*2) + 1/(3*3) + ... + 1/(80*80)   ->
# prod(3 to 80)^2 =           P/(3*3) + ... + P(80*80)

# notice that LHS mod prod(subset(3 to 80))^2 = 0, so this must be true of solutions as well
# let m = prod((p, ..., np)^2 where p is prime and (p, ..., np) are all multiples below 81
# if p is feasible, then for some subset (q_1, ..., q_k) of (p, ..., np):
# we have 0 = P/(q_1)^2 + ... P/(q_k)^2  [mod m]
# if the RHS is != 0 for all subsets, then (p, ..., np) are not part of any solution
# and so p is infeasible and can be ignored

'''
# proof that 23 and its multiples cannot be included
a = math.prod(( n**2 for n in range(2, 81) ))
assert (a//(23**2)                          ) % ((23*46*69)**2) != 0
assert (             a//(46**2)             ) % ((23*46*69)**2) != 0
assert (                          a//(69**2)) % ((23*46*69)**2) != 0
assert (a//(23**2) + a//(46**2)             ) % ((23*46*69)**2) != 0
assert (a//(23**2)              + a//(69**2)) % ((23*46*69)**2) != 0
assert (             a//(46**2) + a//(69**2)) % ((23*46*69)**2) != 0
assert (a//(23**2) + a//(46**2) + a//(69**2)) % ((23*46*69)**2) != 0


# NOT proof for 35 - all fail
# assert (a//(35**2) + a//(70**2)) % ((35*70)**2) != 0
# assert (a//(35**2))              % ((35*70)**2) != 0
# assert (a//(70**2))              % ((35*70)**2) != 0
'''


# create a set of feasible terms
# TODO could use feasible sets to avoid infeasible solutions


common = math.prod(( n**2 for n in range(2, 81) ))
not_feasible = set()
for n in get_primes(80): # range(3, 81)
	if n == 2: 
		continue
	multiples = list(range(n, 81, n))
	mod = math.prod(multiples)**2 # divides common/4, test if it divides the other side
	assert common//4 % mod == 0
	feasible = False
	for s in subsets(multiples):
		if len(s) == 0:
			continue
		b = sum(( common//(x**2) for x in s ))
		if b % mod == 0:
			feasible = True
			# print(f"{n}: P/{s}^2  mod  {multiples}^2  =  0")
			break
	if not feasible:
		for m in multiples:
			not_feasible.add(m)
feasible = set(range(3,81)) - not_feasible
#print(f"not feasible: {not_feasible}")
#print(f"    feasible: {feasible}")
#print(f"len feasible: {len(feasible)}")


# multiply by LCM


feasible = [n**2 for n in sorted(feasible)]
common = reduce(lcm, feasible)
assert common % 4 == 0
target = common // 4 
feasible = [common//n for n in feasible]
#print(f"       terms: {feasible}")


# meet-in-the-middle algorithm


A = feasible[:len(feasible)//2]
B = feasible[len(feasible)//2:]
B = sorted(( (sum(s), s) for s in subsets(B) ))
assert binary_search(B, target, lambda x: x[0]) == (-1, None)
count = 0
for asub in subsets(A):
	asum = sum(asub)
	if asum == target:
		count += 1
		#print([math.floor(math.sqrt(common//n)) for n in asub])
	elif asum < target:
		b_target = target - asum
		mid, bsub = binary_search(B, b_target, lambda x: x[0])
		if mid != -1:
			count += 1
			# some entries in B have same b_target sum
			for i in range(mid + 1, len(B), 1):
				if B[i][0] == b_target:
					count += 1
				else:
					break
			for i in range(mid - 1, -1, -1):
				if B[i][0] == b_target:
					count += 1
				else:
					break
			#print([math.floor(math.sqrt(common//n)) for n in asub], end="")
			#print([math.floor(math.sqrt(common//n)) for n in bsub[1]])

print(f"ans = {count}")