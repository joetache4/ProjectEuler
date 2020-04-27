"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.

ans: 142913828922
"""

from lib.num import is_prime

max = 2000000

sum = 2
k = 3
while k < max:
	if is_prime(k):
		sum += k
	k += 2

print(sum)