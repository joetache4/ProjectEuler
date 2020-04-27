"""
A natural number, N, that can be written as the sum and product of a given set of at least two natural numbers, {a1, a2, ... , ak} is called a product-sum number: N = a1 + a2 + ... + ak = a1 × a2 × ... × ak.

For example, 6 = 1 + 2 + 3 = 1 × 2 × 3.

For a given set of size, k, we shall call the smallest N with this property a minimal product-sum number. The minimal product-sum numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.

k=2: 4 = 2 × 2 = 2 + 2
k=3: 6 = 1 × 2 × 3 = 1 + 2 + 3
k=4: 8 = 1 × 1 × 2 × 4 = 1 + 1 + 2 + 4
k=5: 8 = 1 × 1 × 2 × 2 × 2 = 1 + 1 + 2 + 2 + 2
k=6: 12 = 1 × 1 × 1 × 1 × 2 × 6 = 1 + 1 + 1 + 1 + 2 + 6

Hence for 2≤k≤6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30; note that 8 is only counted once in the sum.

In fact, as the complete set of minimal product-sum numbers for 2≤k≤12 is {4, 6, 8, 12, 15, 16}, the sum is 61.

What is the sum of all the minimal product-sum numbers for 2≤k≤12000?


ans: 7587457
"""


'''
Solution Method

2k is a product-sum number for size k. Note that sum(1,...,1,2,k) = prod(1,...,1,2,k) = 2k
where "1,...1" is a sequence of (k-2) ones.

All product-sum numbers n for a given size k follow n = prod(F) = sum(F) + k - len(F), 
where F is a factorization of n into prime or composite numbers.

So, any given n is a product-sum number of size k = prod(F) - sum(F) + len(F).

Iterate over all n ≤ 2*12000
	Iterate over all F of n
		Calculate k
		Map k -> n if k is not yet mapped
Sum the image of 2≤k≤12000
'''

from math import isqrt

max_val = 12000

def first_divisor(n):
	if n % 2 == 0 and n != 2:
		return 2
	for m in range(3, isqrt(n) + 1, 2):
		if n % m == 0:
			return m
	return None # don't return 1 or n

# get a list of list of all ways to factor n into (prime or composite) numbers
def partitions(n):
	ans = set()
	if n == 1:
		pass
	else:
		d = first_divisor(n)
		if d is None:
			ans.add( (n,) ) # comma makes a tuple, not parentheses
		else:
			for partition in partitions(n//d):					
				for i in range(len(partition)):
					a = list(partition)
					a[i] *= d
					ans.add( tuple(sorted(a)) )
				a = list(partition)
				a.append(d)
				ans.add(tuple(sorted(a)))
	return ans

min_ps_num = {}
for n in range(2, 2*max_val+1):
	for p in partitions(n):
		k = n - sum(p) + len(p)
		if k not in min_ps_num:
			min_ps_num[k] = n

ans = set()
for k in range(2, 12001):
	ans.add(min_ps_num[k])
print(sum(ans))