"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.
HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.

ans: 45228
"""

from math import prod
from lib.num import factor
from lib.list import subsets

def pandigital(num):
	if num < 123456789 or num > 987654321:
		return False
		
	arr = [int(x) for x in str(num)]
	for k in range(1, 10):
		if k not in arr:
			return False
			
	return True
	
p = set()
for n in range(2, 11111):
	factors = factor(n)
	for subset in subsets(factors):
		
		term1 = subset
		
		term2 = factors.copy()
		for t in term1:
			term2.remove(t)
			
		term1 = prod(term1)
		term2 = prod(term2)
		
		if pandigital(int(f"{term1}{term2}{n}")):
			print(f"{term1} {term2} {n}")
			p.add(n)
			break

ans = sum(p)
print(f"ans = {ans}")