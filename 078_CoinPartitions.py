"""
Let p(n) represent the number of different ways in which n coins can be separated into piles. For example, five coins can be separated into piles in exactly seven different ways, so p(5)=7.
OOOOO
OOOO   O
OOO   OO
OOO   O   O
OO   OO   O
OO   O   O   O
O   O   O   O   O

Find the least value of n for which p(n) is divisible by one million.


ans: 55374
"""

from math import sqrt, floor, ceil

def p(n, _mem = {0:1}):
	try:
		return _mem[n]
	except KeyError:
		if n < 0:
			return 0
		elif n == 0:
			return 1
		else:
			ans = 0
			start = -(sqrt(24*n+1)-1)/6
			stop  =  (sqrt(24*n+1)+1)/6
			start = ceil(start)
			stop  = floor(stop)
			for k in range(start, stop + 1, 1):
				q = k*(3*k-1)//2
				if q <= 0:
					continue				
				if (k+1) % 2 == 0:
					ans += p(n - q)
				else:
					ans -= p(n - q)
					
			_mem[n] = ans
			return ans

assert p(5) == 7
assert p(6) == 11
assert p(7) == 15
assert p(8) == 22
assert p(9) == 30
assert p(10) == 42
assert p(11) == 56
assert p(12) == 77
print("*")

n = 1
while p(n) % 10**6 != 0:
	n += 1

print(n)
print(p(n))