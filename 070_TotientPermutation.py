"""
Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine the number of positive numbers less than or equal to n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to nine, φ(9)=6.
The number 1 is considered to be relatively prime to every positive number, so φ(1)=1.

Interestingly, φ(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which φ(n) is a permutation of n and the ratio n/φ(n) produces a minimum.

ans: 8319823=3557*2339, tot=8313928, n/tot=1.0007090511248113
"""

from lib.num import get_primes, is_permutation

max_n = 10**7

# assume there are exactly two prime divisors 
primes = get_primes(max_n // 2)
min_ratio = max_n
for i in range(len(primes)-1, 0, -1):
	a = primes[i]
	for j in range(0, i):
		b = primes[j]
		n = a*b
		if n >= max_n:
			break
		tot = (a-1)*(b-1)
		# we are ignoring numbers whose n/φ(n) is higher than minimum
		if n >= tot*min_ratio:
			continue
		if not is_permutation(n, tot):
			continue
		# This (a,b) MIGHT be the solution, but there could be 
		# subsequent combinations with lower totient values
		min_ratio = n/tot
		print(f"{n} = {a}*{b}, tot={tot}, n/tot={n/tot}")
		