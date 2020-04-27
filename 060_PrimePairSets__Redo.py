"""
The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order the result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four primes, 792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.


ans: 26033
"""

# This is slow and unsatisfying, but my solution here is to 
# make a subset of size 5 from smaller subsets

from lib.num import binary_search, get_primes
from data._primes import get_data

primes = get_primes(10**8)

find   = lambda p: binary_search(primes, p)
concat = lambda a, b: find(int(str(a)+str(b))) != -1
pair   = lambda a, b: concat(a, b) and concat(b, a)
disjoint = lambda a, b: all(( x not in b for x in a ))

ind = [-1, 0, find(11), find(101), find(1009), find(10007), find(100003), find(1000003), find(10000019)]

print("**1")

subset1 = []
subset2 = []
for i in range(ind[5]-1):
	a = primes[i]
	acceptable = False
	for j in range(i+1, ind[5]):
		b = primes[j]
		if pair(a, b):
			acceptable = True
			subset2.append((a,b))
	if acceptable:
		subset1.append(a)

print(len(subset1))
print(len(subset2))
print("**2")

subset4 = set()
for i in range(len(subset2)-1):
	a = subset2[i]
	for j in range(i+1, len(subset2)):
		b = subset2[j]
		if disjoint(a, b):
			if all(( pair(x,y) for x in a for y in b )):
				subset4.add(tuple(sorted(( a[0], a[1], b[0], b[1] ))))
subset4 = sorted(subset4)

print(subset4)
print(len(subset4))
print("**3")

subset5 = []
for a in subset1:
	for b in subset4:
		if a not in b:
			if all(( pair(a,x) for x in b )):
				subset5.append(sorted(( a, b[0], b[1], b[2], b[3] )))

print(subset5)
print(min(( sum(x) for x in subset5 )))