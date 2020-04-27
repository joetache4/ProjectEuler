"""
A positive integer matrix is a matrix whose elements are all positive integers.
Some positive integer matrices can be expressed as a square of a positive integer matrix in two different ways. Here is an example:
(40 48 12 40) = (2 12 3 2)^2 = (6 4 1 6)^2

We define F(N) as the number of the 2x2 positive integer matrices which have a trace less than N and which can be expressed as a square of a positive integer matrix in two different ways.
We can verify that F(50) = 7 and F(1000) = 1019.

Find F(10^7). 

ans: 145159332
"""

# https://en.wikipedia.org/wiki/Square_root_of_a_2_by_2_matrix

import math
from lib.num import get_primes, lcm, extended_gcd, count_divisors
from lib.progressbar import tick

max_trace  = 10**7
max_trace -= 1

squares = []
i = 1
while True:
	squares.append(i*i)
	i += 1
	if i*i > max_trace:
		break

primes = get_primes(max_trace)

def cached_count_divisors(n, primes, cache={}):
	try:
		return cache[n]
	except:
		d = count_divisors(n, primes)
		cache[n] = d
		return d
	

count = 0
for i in range(len(squares)-1):

	#tick(len(squares)-1)
	
	for j in range(i+1, len(squares)):
		s1 = squares[j]
		s2 = squares[i]
		
		tr_m  = s1 + s2
		
		if tr_m > max_trace:
			break # otherwise trace is too big
		
		det_m = s1*s2
		det_r = int(math.sqrt(det_m))
		
		t2 = tr_m + 2*det_r
		t  = int(math.sqrt(t2))
		if t*t != t2:
			continue # otherwise all a+det_r/t, etc. are irrational
		t2_neg = tr_m - 2*det_r
		t_neg  = int(math.sqrt(t2_neg))
		if t_neg*t_neg != t2_neg:
			continue # otherwise all a-det_r/t_neg, etc. are irrational
		
		
		
		# works but slow
		# for a in range(det_r + 1, tr_m - det_r, 1): # so a and d are > det_r
			
		# works but slow
		#start = det_r + 1
		#start = start - (start + det_r) % t + t
		#for a in range(start, tr_m - det_r, t):

		# works but slow
		#start = det_r + 1
		#while start % t != -det_r % t and start < tr_m - det_r:
		#	start += 1
		#while start % t_neg != det_r % t_neg and start < tr_m - det_r:
		#	start += t
		
		
		# from:
		# (a + det_r) % t     = 0
		# (a - det_r) % t_neg = 0
		# (d + det_r) % t     = 0
		# (d - det_r) % t_neg = 0
		# d = tr_m - a
		
		# we have:
		# a = -det_r =  det_r + tr_m (mod t)
		# a =  det_r = -det_r + tr_m (mod t_neg)
		
		# see if both sides are always equal - they are
		#if -det_r % t != (det_r + tr_m) % t or det_r % t_neg != (-det_r + tr_m) % t_neg:
		#	foo()
		
		inc = lcm(t, t_neg) # so above congruences don't change after incrementing
		# find 'start' 
		# generalized Chinese Remainder Theorem says there's a unique solution to
		# the congruence relations mod lcm(t, t_neg)
		g, b1, b2 = extended_gcd(t, t_neg)
		start  = (-det_r % t)*b2*t_neg + (det_r % t_neg)*b1*t
		start //= g
		# now that we have the unique solution, increment (or decrement) it until
		# it is just over det_r + 1
		while start >= det_r + 1: # sometimes, start is higher than needed
			start -= inc
		while start < det_r + 1:
			start += inc
		for a in range(start, tr_m - det_r, inc):
		
			d  = tr_m - a
			if a > d:
				break # symmetry: if (a,b,c,d) is a solution, then so is (d,b,c,a)
			
			bc = a*d - det_m
			
			# not necessary if a and d are > det_r
			#if bc < 1:
			#	continue # otherwise b or c is nonpositive
			
			if bc % (t**2) != 0 or bc % (t_neg**2) != 0:
				continue # otherwise won't have 2 diviors (b and c) divisible by t and t_neg
			
			# these aren't necessary anymore
			#if (a+det_r) % t != 0 or (d+det_r) % t != 0:
			#	continue # otherwise a+det_r/t or d+det_r/t is a fraction
			#if (a-det_r) % t_neg != 0 or (d-det_r) % t_neg != 0:
			#	continue # otherwise a-det_r/t_neg or d-det_r/t_neg is a fraction
			
			bc //= lcm(t**2, t_neg**2)
			
			if a == d:
				count += cached_count_divisors(bc, primes)
			else:
				count += cached_count_divisors(bc, primes) * 2
				
			
			# no longer necessary
			#for b in cached_count_divisors(bc, primes): 
				#if b % t != 0 or b % t_neg != 0:
				#	continue # otherwise fraction				
				#c = bc // b				
				#if c % t != 0 or c % t_neg != 0:
				#	continue # otherwise fraction
				
				#count += 2 # symmetry
				#if a == d:
				#	count -= 1
				
				#print(f"[{a} {b} {c} {d}] [{(a+det_r)//t} {b//t} {c//t} {(d+det_r)//t}] [{(a-det_r)//t_neg} {b//t_neg} {c//t_neg} {(d-det_r)//t_neg}] {s1} {s2} - {det_r + 1} {tr_m - det_r - 1} - {t} {t_neg} - {start} {inc}")
			
			# not correct
			#if a != start:
			#	foo()
		
print(count)