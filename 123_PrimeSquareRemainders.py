"""
Let pn be the nth prime: 2, 3, 5, 7, 11, ..., and let r be the remainder when (pn−1)^n + (pn+1)^n is divided by pn^2.

For example, when n = 3, p3 = 5, and 4^3 + 6^3 = 280 ≡ 5 mod 25.

The least value of n for which the remainder first exceeds 10^9 is 7037.

Find the least value of n for which the remainder first exceeds 10^10.

ans: 21035
"""

# (a+1)^n + (a-1)^n  =  2(c0a^n + c1a^(n-2) + c2a^(n-4) + ...) where c are binomial coefficients
# When n odd,  remainder when divided by a^2 is 2na = 2n(nth prime) = 2n p_n-1
# When n even, remainder when divided by a^2 is 2, so when can ignore these

from lib.num import get_primes

p = get_primes(1000000)

exceed = 10**10

for n in range(1, len(p), 2):
	if 2*n*p[n-1] > exceed:
		print(n)
		break