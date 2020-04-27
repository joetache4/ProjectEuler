"""
Let f(N) be the number of points with integer coordinates that are on a circle passing through (0,0), (N,0),(0,N), and (N,N).

It can be shown that f(10000)=36.

What is the sum of all positive integers N≤10^11 such that f(N)=420?


ans: 271204031455541309
"""


'''
Solution Method

The circle has radius sqrt( n^2 / 2 )

When n is even, count the Gaussian integers a+bi with norm
|a+bi| = a^2 + b^2 = n^2/2. Because n is even, n^2/2 is an integer.

Factor n into Gaussian primes. Note that:
     2 = (1+i)(1-i) = i(1-i)^2
primes = 3 (mod 4) are Gaussian primes
primes = 1 (mod 4) can be factored into exactly 2 Gaussian primes

Distribute the primes of n^2/2 into a 2-column table with conjugate pairs in opposite columns.
Disregard Gaussian primes without an imaginary part.
Disregard 2 (its effect will be captured later).

Multiply the primes in the left column. This Gaussian integer corresponds to 
a point on the circle's edge. By swapping primes and their conjugates, the column product
will change to a new Gaussian integer. 

To get the rest of the points, multiply the previous ones by -1, i, and -i, corresponding to relfection or rotation around the circle's edge. (Because 2 = i(1-i) * (1-i), its effect is captured here).

So, the number of points on the edge is 4*prod(k[i]+1) where each k[i] is 
the power of the prime p[i] in the factorization of n^2, and p[i]%4 == 1.
If this value is 420, then n is part of the solution.

420 = 4 * prod(k[i] + 1)
120 = prod(k[i] + 1)

Because 120 = 3*5*7, k must be one of: {2,4,6}, {14,6}, {4,20}, {34,2}, {104}
So, for n, these exponents are halved: {1,2,3}, {7 ,3}, {2,10}, {17,1}, {52}

Instead of looping through all integers n <= 10^11 and testing its primes,
it is faster to construct all numbers with primes =1 (mod 4) raised to the right powers (above),
multiplied by any amount of primes =3 (mod 4).


When n is odd, n^2/2 is not an integer -- but this isn't a problem. Instead of finding integers
a and b for a+bi, find a and b that are in the middle of two integers (e.g., 1.5, 73.5, etc.).

Let a = c/2 and b = d/2, where c and d are integers.
Remember, the circle is centered at (n/2, n/2). So n/2 + c/2 and n/2 + d/2 are also integers. 

Note n^2/2 = a^2 + b^2 = |a+bi| = |c+di|/2.
So, the problem is to count all integer combinations of c,d such that |c+di|=n^2.
This is done using the same procedure as when n was even.
'''

from math import prod
from lib.num import get_primes

# Returns all numbers <= max that have only the given primes in their factorizations.
def composites(primes, max, _base = 1, _ind = 0):
	for i in range(_ind, len(primes)):
		p = primes[i]
		m = _base * p 
		if m > max:
			break
		yield m
		yield from composites(primes, max, m, i)

# Returns all numbers <= max with len(exps) prime factors in bases, raised to the exponents in exps.
def powers(bases, exps, max, _selected = None):
	if _selected is None:
		_selected = []
	for i in range(len(bases)):	
		if i not in _selected:
			_selected.append(i)
			p = prod((bases[_selected[j]]**exps[j] for j in range(len(_selected))))	
			if p > max:
				_selected.pop()
				break			
			if len(_selected) == len(exps):
				yield p
			else:
				yield from powers(bases, exps, max, _selected)			
			_selected.pop()

primes      = get_primes(10**7)
primes_1mod = [p for p in primes if p%4 == 1]
primes_3mod = [p for p in primes if p%4 == 3 or p == 2] # 2 is treated the same as others here

ans = 0
for exp in [(3,2,1), (7,3), (10,2), (17,1)]: # ignore [52] for being too big
	for n in powers(primes_1mod, exp, (10**11)):
		ans += n		
		ans += n * sum(composites(primes_3mod, (10**11)//n))

print(ans)