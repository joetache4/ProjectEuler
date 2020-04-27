"""
NOTE: This is a more difficult version of Problem 114.

A row measuring n units in length has red blocks with a minimum length of m units placed on it, such that any two red blocks (which are allowed to be different lengths) are separated by at least one black square.

Let the fill-count function, F(m, n), represent the number of ways that a row can be filled.

For example, F(3, 29) = 673135 and F(3, 30) = 1089155.

That is, for m = 3, it can be seen that n = 30 is the smallest value for which the fill-count function first exceeds one million.

In the same way, for m = 10, it can be verified that F(10, 56) = 880711 and F(10, 57) = 1148904, so n = 57 is the least value for which the fill-count function first exceeds one million.

For m = 50, find the least value of n for which the fill-count function first exceeds one million.

ans:
"""

mem = {}

def F(m, length):
	return F_r(True, m, length) + F_r(False, m, length)

def F_r(red, m, length):
	if red:
		if length == m:
			return 1
		elif length < m:
			return 0
	else:
		if length == 1:
			return 1
		elif length < 1:
			return 0
	
	if (red, length) in mem:
		return mem[(red, length)]
	
	count = 1
	if red:
		for i in range(m, length+1):
			count += F_r(False, m, length-i)
	else:
		for i in range(1, length+1):
			count += F_r(True, m, length-i)
	
	mem[(red,length)] = count
	return count

assert F(3,7) == 17
mem = {}
assert F(10,57) == 1148904
mem = {}

for n in range(100,1000):
	if F(50, n) > 10**6:
		print(n)
		break

mem = {}
assert F(50, 167) <= 10**6 and F(50, 168) > 10**6