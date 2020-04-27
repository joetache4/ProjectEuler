"""
The 5-digit number, 16807=75, is also a fifth power. Similarly, the 9-digit number, 134217728=89, is a ninth power.

How many n-digit positive integers exist which are also an nth power?

ans: 49
"""

count = 0
p = 1
while True:
	n = 1
	while True:
		m = n**p
		l = len(str(m))
		if l == p:
			count += 1
		elif l > p:
			break
		n += 1
	p += 1
	if len(str(9**p)) < p:
		break

print(count)