"""
It is well known that if the square root of a natural number is not an integer, then it is irrational. The decimal expansion of such square roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first one hundred decimal digits for all the irrational square roots.


ans: 40886
"""

# cheesed using the decimal class

import decimal

decimal.getcontext().prec = 102

sum = 0
for n in range(1, 101):
	n = decimal.Decimal(n).sqrt()
	n = str(n)
	if "." in n:		
		for d in n.replace(".","")[:100]:
			sum += int(d)
print(sum)



# Babylonian Method
# https://en.wikipedia.org/wiki/Methods_of_computing_square_roots

decimal.getcontext().prec = 110
D = decimal.Decimal
squares = [x**2 for x in range(1,11)]
sum = 0
for n in range(1, 101):
	if n not in squares:
		sr = D(n)/2
		for i in range(10):
			sr = (sr + n/sr)/2
		for d in str(sr).replace(".","")[:100]:
			sum += int(d)
print(sum)