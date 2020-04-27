"""
Consider quadratic Diophantine equations of the form:

x2 – Dy2 = 1

For example, when D=13, the minimal solution in x is 6492 – 13×1802 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

32 – 2×22 = 1
22 – 3×12 = 1
92 – 5×42 = 1
52 – 6×22 = 1
82 – 7×32 = 1

Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.

Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.

ans: 661
"""

# This is Pell's equation.
	# See: https://en.wikipedia.org/wiki/Pell's_equation
# My original solution method involved the convergents of the continued fraction for sqrt(n).
	# See: https://en.wikipedia.org/wiki/Continued_fraction#Infinite_continued_fractions_and_convergents
	# However, sqrt(n) has limited precision, making the fraction inaccurate after about 20 - #digits(n) iterations. This was insufficient to solve certain numbers, starting with D=61.
# My final, working solution method involves the Chakravala Method.
	# See: https://en.wikipedia.org/wiki/Chakravala_method
	# 1. Start with a triplet (a, b, k) s.t. a^2 -nb^2 = k and gcd(a,b)=1
	# 2. Choose positive int m s.t. (a+bm)/k is an int and abs(m^2 - n) is minimized
	# 3. "Compose" (a,b,k) with (m,1,m^2-n) to get a new triplet
	# 4. Divide the new triplet by the old k (Bhaskara's Lemma)
	# 5. Repeat steps 2-4 until a triplet with k=1 is found

import sys
from math import *

max_val = 1000
try:
	max_val = int(sys.argv[1])
except:
	pass

# final solution method
def chakravala_method(n):
	a = 10
	b = 1
	k = a*a - n
	
	while k != 1:		
		# choose m
		s = floor(sqrt(n))
		candidates = []
		for c in range(s+1, s+abs(k)+1):
			if (a + b*c) % k == 0:
				candidates.append(c)
				break
		for c in range(s-1, max(1, s-abs(k)-1), -1):
			if (a + b*c) % k == 0:
				candidates.append(c)
				break
		# print(candidates)
		m = min(candidates, key = lambda x: abs(x*x - n))	

		# print(f"|m^2 - {n}| minimized by m={m} where k={k} divides {a}+{b}m (sqrt(n)~{floor(sqrt(n))})")
		# assert (a*m + n*b) % k == 0
		# assert (a + b*m) % k == 0
		# assert (m*m - n) % k == 0
		
		# this was verified when a much larger search window was used
		# verifying this helped narrow the window
		# assert abs(abs(m)-s) <= abs(k)
		
		# compose (a,b,k) with (m, 1, m^2 - n), scale down by k
		a, b, k = (a*m + n*b)//abs(k),  (a + b*m)//abs(k),  (m*m - n)//k
	
	assert a*a - n*b*b == 1
	return (a,b)

def main_using_chakravala(max_val):
	max_x = -1
	max_d = -1
	for d in range(max_val+1):
		# skip perfect squares
		tmp = sqrt(d)
		if tmp == int(tmp):
			continue
		# find minimal solution for Pell's Equations of d
		sol = chakravala_method(d)
		# print(f"{d}: {sol}")
		if sol[0] > max_x:
			max_x = sol[0]
			max_d = d

	print(f"d = {max_d} when x is maximized among minimal solutions involving d < {max_val+1} (x = {max_x})")

assert chakravala_method(61) == (1766319049, 226153980)
assert chakravala_method(67) == (48842, 5967)

main_using_chakravala(max_val)



# My original method is included below for the curious. It is not referenced by the above code.



# Not accurate after about 20 - #digits(n) iterations; not good enough to solve n = 61.
# n cannot be square.
def convergents(n):
	a = sqrt(n)
	b = floor(a) # b is each term in the continued fraction for sqrt(n)
	if a == b:
		raise ValueError()
	# convergents can be calculated by keeping record of the last two results
	prev2 = (1, 0)
	prev1 = (b, 1)
	yield prev1
	for i in range(20):
		a = 1/(a - b)
		b = floor(a)
		current = (b*prev1[0] + prev2[0], b*prev1[1] + prev2[1])
		yield current
		prev2 = prev1
		prev1 = current
	raise FloatingPointError("Precision is lost.")
	
def main_using_convergents():
	max_x = -1
	max_d = -1
	for d in range(max_val+1):
		try:
			for (x,y) in convergents(d):
				if x*x - d*y*y == 1:
					print((x,y))
					# solution found for d
					if x > max_x:
						max_x = x
						max_d = d
					break
		except ValueError:
			# d was square - ignore
			pass
		except FloatingPointError:
			print(f"error for d = {d}")
			sys.exit()
	print(f"d = {d} when x is maximized among minimal solutions with d < {max_val+1} (x,y = {x},{y})")