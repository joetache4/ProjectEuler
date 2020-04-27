"""
Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d ≤ 1,000,000 in ascending order of size, find the numerator of the fraction immediately to the left of 3/7.

ans: 428570
"""

from math import ceil
from lib.num import gcd

min_diff = 9999999999
min_n = 0
min_d = 0

for d in range(2, 1000001):
	n = ceil(3*d/7 - 1)
	diff = 3 - 7*n/d
	if diff < min_diff:
		min_diff = diff
		min_n = n
		min_d = d

g = gcd(min_n, min_d)
print(f"frac = {min_n//g}/{min_d//g}")
print(f"diff = {3/7 - min_n/min_d}")
print(f"ans  = {min_n//g}")
