"""
It turns out that 12 cm is the smallest length of wire that can be bent to form an integer sided right angle triangle in exactly one way, but there are many more examples.

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer sided right angle triangle, and other lengths allow more than one solution to be found; for example, using 120 cm it is possible to form exactly three different integer sided right angle triangles.

120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L ≤ 1,500,000 can exactly one integer sided right angle triangle be formed?


ans: 161667
"""


# https://en.wikipedia.org/wiki/Pythagorean_triple#Generating_a_triple

from collections import Counter
from lib.num import gcd

max = 1500000

counter = Counter()
m = 2

while True:
	
	n_start, n_inc = (1,1) if m%2 == 0 else (2,2)

	for n in range(n_start, m, n_inc):
		
		if gcd(m,n) != 1:
			continue
		
		a = m*m - n*n
		b = 2*m*n
		c = m*m + n*n
		L = a + b + c
		
		if L > max:
			break
		
		k = 1
		while k*L <= max:
			counter[k*L] += 1
			k += 1
		
	m += 1
	if 2*m*m + 2*m > max:
		break
			
print(sum((1 for k,v in counter.items() if v == 1)))



# Also works, but slower

'''
from math import sqrt
from collections import Counter

max = 1500000

s =set()

for r in range(2, int(sqrt(max))):
	for i in range(1, r):
		g = complex(r, i)
		g *= g
		
		a = int(abs(g.real))
		b = int(abs(g.imag))
		c = int(abs(g))
		
		L = a + b + c
		if L > max:
			break
		
		d = sorted((a,b,c))
		k = 1
		while k*L <= max:
			s.add((k*d[0], k*d[1], k*d[2]))
			k += 1

counter = Counter()
for a in s:
	counter[sum(a)] += 1
print(sum((1 for k,v in counter.items() if v == 1)))
'''