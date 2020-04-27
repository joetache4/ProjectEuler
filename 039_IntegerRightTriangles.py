"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximized?

ans: There are 16 Pythagorean triplets with perimeter 840.
"""

import sys
from math import sqrt
from random import randint
from lib.num import gcd

n = 1000
do_test = False

# input is either a number (n) or the word "test"

if len(sys.argv) > 1:
	if sys.argv[1] == "test":
		do_test = True
	else:
		n = int(sys.argv[1])

def farey(n):
	"""Use Farey sequences to generate list of coprime numbers."""
	a, b, c, d = 0, 1, 1, n
	while c <= n:
		k = (n + b) // d
		a, b, c, d = c, d, (k*c-a), (k*d-b)
		if (a == 1 and b == 1): break
		yield (a,b)

# TODO return in standard order, a < b < c ?
def triplet(m, n):
	"""Use Euclid's method to generate primitive Pythagorean triplets."""
#	if m <= n or (m%2 == 1 and n%2 == 1):
#		# m > n, not both odd
#		raise Exception("Bad m,n for generating primitive Pythagorean triplets")
	a = m*m - n*n
	b = 2*m*n
	c = m*m + n*n
	return (a, b, c)

		
def test():
	print("Testing...")
	# test farey()
	assert [(a,b) for (a,b) in farey(3)] == [(1, 3), (1, 2), (2, 3)]
	for i in range(100):
		n = randint(2, 100)
		nums = [(a,b) for (a,b) in farey(n)]
		for j in range(100):
			a = randint(1, n-1)
			b = randint(a + 1, n)
			g = gcd(a, b)
			a //= g
			b //= g
			assert (a, b) in nums
	
	# test triplet()
	for i in range(10000):
		n = randint(1, 999)
		m = randint(n + 1, 1000)
		g = gcd(m, n)
		m //= g
		n //= g
		if m % 2 == 1 and n % 2 == 1:
			m *= 2
		a, b, c = triplet(m, n)
		assert gcd (a, b) == 1 or gcd (b, c) == 1
		assert a*a + b*b == c*c
		
	# test main() given details in prompt
	assert main(120) == (120, 3)
		
	print("[SUCCESS]")
		
def main(p_max):
	triplets = set()
	# calculate the Farey order needed so only a few triplets are generated with perimeter > p_max
	f_order = int(sqrt(p_max / 2)) + 1
	# find all Pythagorean triplets
	for (n, m) in farey(f_order):
		if m%2 == 0 or n%2 == 0: # m > n is assumed
			a, b, c = triplet(m, n)	
			if a > b:
				a, b = b, a
			#if a+b+c > p_max: print((a,b,c))
			scaled_a, scaled_b, scaled_c = a, b, c
			# scale each triplet and add to the set
			# some Pythagorean triplets ARE scaled multiples of several primitive triplets
			while scaled_a + scaled_b + scaled_c <= p_max:
				triplets.add((scaled_a, scaled_b, scaled_c)) # no need to swap a and b
				scaled_a += a 
				scaled_b += b 
				scaled_c += c
	# group according to perimeter
	num_solutions = {}
	for (a, b, c) in triplets:
		p = a + b + c
		if p not in num_solutions: num_solutions[p] = 0
		num_solutions[p] += 1
	# find perimeter with max number of solutions
	max_key = p_max
	max_val = 0
	for k in num_solutions.keys():
		if num_solutions[k] > max_val:
			max_key = k
			max_val = num_solutions[k]
			
	return (max_key, max_val)
		
if do_test:
	test()
else:
	max_key, max_val = main(n)
	print("There are {} Pythagorean triplets with perimeter {}.".format(max_val, max_key))