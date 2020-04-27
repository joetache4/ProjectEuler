"""
The number of divisors of 120 is 16.
In fact 120 is the smallest number having 16 divisors.

Find the smallest number with 2^500500 divisors.
Give your answer modulo 500500507.


ans: 35407281
"""

'''
Solution Method

Let n = sum(p[i] ^ a[i])
In order to have 2^500500 divisors, prod(1 + a[i]) = 2^500500
This means every 1 + a[i] is a power of 2.
Let a[i] = 2^k[i] - 1.
So, sum(k[i]) = 500500  ->  2^500500 divisors.

Each increment produces exactly 2x more divisors:
delta(divs) = prod(1 + a[i]_final) / prod(1 + a[i]_init)
            = 2^(k[i]+1) / 2^k[i]
			= 2

Solution is to greedily increment k[i] that has the smallest increase to n

The change in n after incrementing k[i]:
delta(n) = p[i]^( 2^(k[i]+1)) / p[i]^(2^k[i] )
         = p[i]^( log(p[i]^(2^(k[i]+1))) - log(p[i]^(2^k[i])) )
         = p[i]^( 2^(k[i]+1) - 2^k[i] )
         = p[i]^( 2^k[i] )

In order to choose the correct k[i], we need to be able to quickly compare values:
    a^(2^b) > c^(2^d)
 2^b*log(a) > 2^d*log(c)
(2^b)/(2^d) > log(c)/log(a)
    2^(b-d) > log_a(c)
'''

import math
from lib.num import mod_pow
from _data._primes import get_data

p = get_data()[:500500]
k = [0 for i in range(len(p))]
k[0] = 1
klen = 1

for i in range(500500-1): # one increment has already been done above	
	min_index = 0
	exp = k[0]
	
	for j in range(1, klen):		
		d = k[j]		
		if d != exp:
			exp = d			
			a = p[min_index]
			b = k[min_index]
			c = p[j]					
			if 2**(b-d) > math.log(c, a):
				min_index = j				
			if exp == 1:
				break
	
	# compare to first prime with k[i] = 0
	a = p[min_index]
	b = k[min_index]
	c = p[klen]
	d = k[klen]
	if 2**(b-d) > math.log(c, a):
		min_index = klen
		klen += 1		
	k[min_index] += 1

m = 500500507
ans = 1
for i in range(klen):
	ans = (ans * mod_pow(p[i], 2**k[i]-1, m)) % m
print(ans)

