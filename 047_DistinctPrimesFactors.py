"""
The first two consecutive numbers to have two distinct prime factors are:

14 = 2 × 7
15 = 3 × 5

The first three consecutive numbers to have three distinct prime factors are:

644 = 2^2 × 7 × 23
645 = 3 × 5 × 43
646 = 2 × 17 × 19.

Find the first four consecutive integers to have four distinct prime factors each. What is the first of these numbers?

ans: 134043
"""

from lib.num import factor

target = 4

def find(target):
	num = 2
	consec = 0
	while consec < target:
		num_primes = len(set(factor(num)))
		if num_primes == target:
			consec += 1
		else:
			consec = 0
		num += 1
	return num - target

print(find(target))