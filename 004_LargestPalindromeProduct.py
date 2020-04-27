"""
Largest palindrome product of two 3-digit ints

ans: 906609 = 913 * 993
"""

def palindrome(n):
	reversed = list(str(n))
	reversed.reverse()
	reversed = "".join(reversed)
	reversed = int(reversed)
	return reversed == n
	
a = 100
b = 100
maxa = a
maxb = b
maxprod = a * b
while (a < 1000):
	b = a
	while (b < 1000):
		prod = a * b
		if (prod > maxprod and palindrome(prod)):
			maxprod = prod
			maxa = a
			maxb = b
		b += 1
	a += 1

print("{} = {} * {}".format(maxprod, maxa, maxb))