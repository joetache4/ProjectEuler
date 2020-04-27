"""
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
a^2 + b^2 = c^2

For example, 3^2 + 4^2 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.

ans: 31875000 (200 * 375 * 425)
"""

squares = [x*x for x in range(1000)]

def main():
	a = 1
	b = 2
	c = -1
	while a < 500:
		while b < 500:
			a2 = a*a
			b2 = b*b
			c2 = a2 + b2
			
			if a2 + b2 + c2 + 2*a*b > 1000000:
				break
				
			if c2 in squares:
				c = squares.index(c2)
				if a + b + c == 1000:
					return a, b, c
					
			b += 1
			
		a += 1
		b = a + 1
		
	raise Exception("error")
	
a, b, c = main()
print(a*b*c)