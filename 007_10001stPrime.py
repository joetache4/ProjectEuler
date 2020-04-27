"""
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10001st prime number?

ans: 104743
"""

from lib.num import is_prime

n = 10001
m = 0

k = 1
while(True):
	if (is_prime(k)):
		m += 1
		if (m == n):
			break
	k += 1

print(k)