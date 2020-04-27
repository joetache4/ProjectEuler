"""
Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13 ≈ 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed. If this process is continued, what is the side length of the square spiral for which the ratio of primes along both diagonals first falls below 10%?

ans:
"""

from lib.num import is_prime

def corners():
	dif = 2
	val = 1
	while True:
		yield (val + dif, val + 2*dif, val + 3*dif, val + 4*dif, dif+1)
		val += 4*dif
		dif += 2

def inc(val, prime, not_prime):
	if is_prime(val):
		prime += 1
	else:
		not_prime += 1
	return prime, not_prime

prime = 0
not_prime = 0

for a, b, c, d, side in corners():
	prime, not_prime = inc(a, prime, not_prime)
	prime, not_prime = inc(b, prime, not_prime)
	prime, not_prime = inc(c, prime, not_prime)
	prime, not_prime = inc(d, prime, not_prime)
	if not_prime > 0 and prime / (prime + not_prime + 1) < 0.1:
		print(side)
		break