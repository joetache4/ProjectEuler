"""

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d ≤ 12,000?

ans: 7295372

"""

# This works but is inefficient:

'''
from lib.num import gcd

count = 0

for d in range(2, 12001):
	for n in range(1, d):
		if gcd(n,d) == 1:
			f = n/d
			if f > 1/3 and f < 1/2:
				count += 1

print(count)
'''



import math
from lib.num import factor, get_primes
from lib.list import subsets

primes = get_primes(12001)

count = 0

# inclusive of bounds
def count_multiples_in_range(lower, upper, n):
	count = upper//n - lower//n
	if lower % n == 0:
		count += 1
	return count

assert count_multiples_in_range(0,2,2) == 2
assert count_multiples_in_range(2,4,2) == 2
assert count_multiples_in_range(3,6,3) == 2
assert count_multiples_in_range(4,7,3) == 1
assert count_multiples_in_range(2,6,3) == 2
assert count_multiples_in_range(2,6,7) == 0
assert count_multiples_in_range(7,15,7) == 2
assert count_multiples_in_range(8,15,7) == 1

for d in range(2, 12001):
	# count acceptable numerators
	upper  = math.ceil(d/2 - 1) 
	lower  = math.floor(d/3 + 1) 
	count += upper - lower + 1
	
	# discount numerators n that share a factor with d (i.e. not reduced)	
	subs = subsets(list(set(factor(d, primes))))
	for s in subs:
		if s != []:
			fact = math.prod(s)
			sign = (-1)**len(s)
			count += sign * count_multiples_in_range(lower, upper, fact)

print(count)