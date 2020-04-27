"""
Euler discovered the remarkable quadratic formula:

n^2+n+41

It turns out that the formula will produce 40 primes for the consecutive integer values 0≤n≤39. However, when n=40,40^2+40+41=40(40+1)+41 is divisible by 41, and certainly when n=41, 41^2+41+41 is clearly divisible by 41.

The incredible formula n^2−79n+1601 was discovered, which produces 80 primes for the consecutive values 0≤n≤79. The product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form:

    n^2+an+b, where |a|<1000 and |b|≤1000

where |n| is the modulus/absolute value of n, e.g. |11|=11 and |−4|=4.

Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n=0.

ans: ab = -59231 (a=-61, b=971, primes=71)
"""

from lib.num import get_primes

primes = get_primes(10**5) # assume we only need primes under 100,000
max_prime = primes[-1]

# Allow negative numbers? If no, then:
# b cannot be negative - this would produce negative numbers at n = 0.
# Additionally, b > -n^2-an. Using calculus to find the maximum of f(n) = -n^2-an,
# we see that b > a^2/4. 

max_a = None
max_b = None
max_prime_count = 0

for a in range(-999, 1000):
	for b in range(a*a//4, 1001):
		prime_count = 0
		for n in range(80):
			f = n*n + a*n + b
			if f > max_prime:
				raise Exception("need to generate more primes")
			if f in primes:
				prime_count += 1
			else:
				break
		if prime_count > max_prime_count:
			max_prime_count = prime_count
			max_a = a
			max_b = b
		if a == -79 and b == 1601:
			print(prime_count)

print(f"ab = {max_a*max_b} (a={max_a}, b={max_b}, primes={max_prime_count})")