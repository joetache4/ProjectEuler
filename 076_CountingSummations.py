"""
It is possible to write five as a sum in exactly six different ways:

4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?

ans: 190569291
"""

# https://en.wikipedia.org/wiki/Partition_(number_theory)

def p(n):
	return sum(( pk(k,n) for k in range(1,n+1) )) - 1

mem = {}
def pk(k,n):
	if k == 0 and n == 0:
		return 1
	if k <= 0 or n <= 0:
		return 0
	if (k,n) in mem:
		return mem[(k,n)]
	val = pk(k, n-k) + pk(k-1, n-1)
	mem[(k,n)] = val
	return val

print(p(100))