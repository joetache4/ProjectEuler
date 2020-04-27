import sys
import math
from random import randint
from collections import Counter
from queue import PriorityQueue

from .array import subsets

#########################################################################################
# helpers

# Convenient wrapper to make any function memoized (including recursive functions).
# hash_func describes how to make a dictionary key from the args given to func.
# This is useful when func is normally given unhashable args, like lists and other collections.
def memoize(func, hash_func = lambda *x: tuple(x)):
	m = {}
	def _memo(*args):
		try:
			return m[hash_func(*args)]
		except KeyError:
			f = func(*args)
			m[hash_func(*args)] = f
			return f
		except RecursionError:
			print("RecursionError in memoized function.")
			sys.exit(1)
	return _memo


#########################################################################################
# simple math

def is_square(x):
	if x < 0:
		return False
	if isinstance(x, float):
		if x % 1 != 0:
			return False
		x = int(x)
	return x == math.isqrt(x)**2 # round(sqrt(x))**2 can fail due to loss of precision

def factorial(n):
	return math.prod(( k for k in range(2, n+1) ))

def choose(a, b):
	prod = 1
	for x in range(a, a-b, -1):
		prod *= x
	for x in range(b, 1, -1):
		prod //= x
	return prod

def mod_pow(base, exp, mod):
	if exp == 0:
		if base == 0:
			raise ValueError("0^0")
		return 1
	elif exp == 1:
		return base
	elif exp % 2 == 0:
		tmp = mod_pow(base, exp//2, mod)
		return (tmp * tmp) % mod
	else:
		tmp = mod_pow(base, exp - 1, mod)
		return (base * tmp) % mod

def base(n, b):
	if n == 0:
		return [0]
	digits = []
	while n:
		digits.append(n % b)
		n //= b
	return digits[::-1]

def is_permutation(a, b):
	if a == 0 and b == 0:
		return True
	if a < 0 or b < 0:
		raise ValueError("Invalid negative argument(s)")
	return sorted(str(a)) == sorted(str(b))

# see https://math.stackexchange.com/questions/495119/what-is-gcd0-0
def gcd(a, b):
	while a != 0 and b != 0:
		if a > b:
			a %= b
		else:
			b %= a
	if a == 0:
		return b
	else:
		return a

# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
def extended_gcd(a, b):
	s, old_s = 0, 1
	t, old_t = 1, 0
	r, old_r = b, a

	while r != 0:
		quotient = old_r // r
		old_r, r = r, (old_r - quotient * r)
		old_s, s = s, (old_s - quotient * s)
		old_t, t = t, (old_t - quotient * t)

	return old_r, old_s, old_t # gcd, Bezout coefficients

def lcm(a, b):
	if a == 0 or b == 0:
		return 0
	return a * b // gcd(a, b)

'''
def is_square(n):
	# Trivial checks
	if not isinstance(n, int):
		if n % 1 != 0:
			return False
		else:
			n = int(n)
	if n < 0:
		return False
	if n == 0:
		return True

	# Reduction by powers of 4 with bit-logic
	while n & 3 == 0:	
		n >>= 2
	# All perfect squares, in binary, end in 001, when powers of 4 are factored out.
	if n & 7 != 1:
		return False
	if n == 1:
		return True  # is power of 4, or even power of 2

	# Simple modulo equivalency test
	c = n % 10
	if c in {3, 7}:
		return False  # Not 1,4,5,6,9 in mod 10
	if n % 7 in {3, 5, 6}:
		return False  # Not 1,2,4 mod 7
	if n % 9 in {2,3,5,6,8}:
		return False
	if n % 13 in {2,5,6,7,8,11}:
		return False

	# Other patterns
	if c == 5:  # if it ends in a 5
		if (n//10)%10 != 2:
			return False	# then it must end in 25
		if (n//100)%10 not in {0,2,6}:
			return False	# and in 025, 225, or 625
		if (n//100)%10 == 6:
			if (n//1000)%10 not in {0,5}:
				return False	# 0625 or 5625
	else:
		if (n//10)%4 != 0:
			return False	## (4k)*10 + (1,9)

	# Babylonian Algorithm. Find the integer square root.
	s = (len(str(n))-1) // 2
	x = (10**s) * 4
	A = {x, n}
	while x * x != n:
		x = (x + (n // x)) >> 1
		if x in A:
			return False
		A.add(x)
	return True
'''

#########################################################################################
# prime numbers

def is_prime(n, primes = None):
	if primes is None:
		return is_prime_trial_division(n)
	else:
		return all((n % p != 0 for p in primes))

def is_prime_trial_division(n):
	if (n < 3):
		if (n == 2):
			return True
		if (n == 1 or n == 0):
			return False
		return is_prime(-n)
	elif (n % 2 == 0):
		return False
	else:
		k = 3
		while k*k <= n:
			if n % k == 0:
				return False
			else:
				k += 2
		return True

# does not include 1 (with the following exception)
# includes n only if n is prime, 0, or 1
def factor(n, primes = None):
	if n in [0,1]:
		return [n]
	# trial division
	if primes == None:
		factors = []
		while(n % 2 == 0):
			factors.append(2)
			n //= 2
		f = 3
		while(f*f <= n):
			if (n % f == 0):
				factors.append(f)
				n //= f
			else:
				f += 2
		if n != 1:
			factors.append(n)
		return factors
	# test each prime
	else:
		factors = []
		for p in primes:
			while n % p == 0:
				factors.append(p)
				n //= p
			if n == 1:
				return factors
		# primes list was not large enough
		raise ValueError("primes list is too small")

def coprime(a, b):
	return gcd(a, b) == 1

def sieve_ero(n):
	primes = [True for x in range(n+1)]
	primes[0] = False
	primes[1] = False
	for k in range(2, n // 2 + 1):
		if not primes[k]:
			continue
		not_prime = k * k
		while not_prime <= n:
			primes[not_prime] = False
			not_prime += k
	return primes

def get_primes(max, sieve = sieve_ero):
	is_prime = sieve(max)
	primes = []
	for k in range(len(is_prime)):
		if is_prime[k]:
			primes.append(k)
	return primes

def totient(n, primes = None):
	if n in [0,1]:
		return n
	fac = set(factor(n, primes))
	for p in fac:
		n *= (1 - 1/p)
	return int(n)

# a number 'a' is a divisor of n if there exists a nonzero number 'b'
# such that a*b = n
# includes all divisors, including 1 and n
def divisors(n, primes = None):
	if n == 0:
		return None
	if n < 0:
		raise ValueError("must be positive")
	div = set([1,n])
	fac = factor(n, primes)
	for sub in subsets(fac):
		div.add(math.prod(sub))
	return div

def count_divisors(n, primes = None):
	if n < 0:
		raise ValueError("must be positive")
	if n in [0,1]:
		return n
	fac = factor(n, primes)
	n = 1
	for k, v in Counter(fac).items():
		n *= (v + 1)
	return n


#########################################################################################
# Gaussian integers
# https://stackoverflow.com/questions/2269810/whats-a-nice-method-to-factor-gaussian-integers
# https://math.stackexchange.com/questions/1562858/gaussian-prime-factorization

def gaussian_remainder(a, b):
	r = a / b
	r = complex(round(r.real), round(r.imag))
	return a - r * b

def gaussian_gcd(a, b):
	r = gaussian_remainder(a, b)
	if r == complex(0,0):
		return b
	else:
		return gaussian_gcd(b, r)

def gaussian_factor_prime(p):
	if p == 2:
		return [complex(1,1), complex(1,-1)]
	elif p % 4 == 3:
		return [complex(p,0)] # irreducible
	else:
		k = None
		while True:
			k = randint(2, p-1)
			if (k**((p-1)//2)) % p == p - 1:
				k = k**((p-1)//4) % p
				break
		f = gaussian_gcd(complex(p,0), complex(k,1))
		return [f, f.conjugate()]

# TODO test this
def gaussian_factor(n, primes = None):
	if n.imag == 0:
		fac = []
		for p in factor(n, primes):
			for g in gaussian_factor_prime(p):
				fac.append(g)
		return fac

	else:
		n = n*n.conjugate()
		gfac = []
		skip = False
		for p in sorted(factor(n, primes)):
			if p == 2:
				q = complex(1,1)
			elif p % 4 == 3:
				if skip:
					skip = False
				else:
					q = complex(p,0) # irreducible and a factor of n
					skip = True	  # skip duplicate made by squaring
			else:
				k = None
				while True:
					a = randint(2, p-1)
					if (a**((p-1)//2)) % p == p - 1:
						k = a**((p-1)//4)
						break
				q = gaussian_gcd(complex(p,0), complex(k,1))
				if gaussian_remainder(n, q) != 0:
					q = q.conjugate()

			gfac.append(q)
			n /= q

		gfac[-1] = gfac[-1] * n # fix signs
		return gfac


#########################################################################################
# Numbers and Sequences

# less than, not including, upper
def _figurative(upper, f):
	n = 1
	while True:
		v = f(n)
		if v < upper:
			yield v
		else:
			break
		n += 1

def triangular(upper = float("Inf")):
	yield from _figurative(upper, lambda n: n*(n+1)//2)

def square(upper = float("Inf")):
	yield from _figurative(upper, lambda n: n*n)

def pentagonal(upper = float("Inf")):
	yield from _figurative(upper, lambda n: n*(3*n-1)//2)

def hexagonal(upper = float("Inf")):
	yield from _figurative(upper, lambda n: n*(2*n-1))

def heptagonal(upper = float("Inf")):
	yield from _figurative(upper, lambda n: n*(5*n-3)//2)

def octagonal(upper = float("Inf")):
	yield from _figurative(upper, lambda n: n*(3*n-2))

# Generate Pythagorean Triples in increasing size of hypotenuse.
# Optionally, yield primitive triples or all triples.
# Note that if (a,b,c) is yielded at some point, then (b,a,c) will NOT be.
def pythag(primitive_only = True):
	pq = PriorityQueue()
	visited = set()
	sides = lambda k,m,n: (k*(m*m - n*n), 2*k*m*n, k*(m*m + n*n))
	pq.put((5,3,4,1,2,1)) # c, a, b, k, m, n
	while True:
		c,a,b,k,m,n = pq.get()
		yield (a,b,c)
		
		if not primitive_only:
			a,b,c = sides(k+1,m,n)
			if (a,b,c) not in visited:
				visited.add((a,b,c))
				pq.put((c,a,b,k+1,m,n))
		
		a,b,c = sides(k,m+1,n)
		if (a,b,c) not in visited:
			visited.add((a,b,c))
			pq.put((c,a,b,k,m+1,n))
		
		if n + 1 < m:
			a,b,c = sides(k,m,n+1)
			if (a,b,c) not in visited:
				visited.add((a,b,c))
				pq.put((c,a,b,k,m,n+1))

def fibonacci(init = (0,1)):
	a,b = init
	while True:
		yield a
		a,b = b,a+b

# https://jamesmccaffrey.wordpress.com/2020/07/30/computing-a-stirling-number-of-the-second-kind-from-scratch-using-python/
def stirling2(n, k):
	s = 0
	for i in range(0, k+1):
		a = (-1) ** (k-i)
		b = choose(k, i)
		c = i ** n
		s += a * b * c
	return s // factorial(k)