"""
There are exactly ten ways of selecting three from five, 12345:

123, 124, 125, 134, 135, 145, 234, 235, 245, and 345

In combinatorics, we use the notation, (5 3)=10

In general, (nr)=n!r!(n−r)!, where r≤n, n!=n×(n−1)×...×3×2×1, and 0!=1

It is not until n=23 that a value exceeds one-million: (2310)=1144066

How many, not necessarily distinct, values of (nr)
for 1≤n≤100, are greater than one-million?

ans: 4075
"""

count = 0

pt = [1]

for r in range(100):
	pt2 = [1]
	for i in range(1, len(pt)):
		n = pt[i] + pt[i-1]
		if n > 10**6:
			count += 1
		pt2.append(n)
	pt2.append(1)
	pt = pt2

print(count)