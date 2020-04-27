"""
The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.

ans: 100
"""

from lib.num import gcd

def test(n, d):
	if n%10 == 0 and d%10 == 0:
		return False
	
	n = str(n)
	d = str(d)
	
	eq = lambda n1, d1, n2, d2: int(n1)*int(d2) == int(n2)*int(d1)
	
	if n[0] == d[0] and eq(n, d, n[1], d[1]):
		return True
	if n[0] == d[1] and eq(n, d, n[1], d[0]):
		return True
	if n[1] == d[0] and eq(n, d, n[0], d[1]):
		return True
	if n[1] == d[1] and eq(n, d, n[0], d[0]):
		return True
	
	return False

prod_n = 1
prod_d = 1

for d in range(11, 99):
	for n in range(10, d):
		if test(n, d):
			print((n, d))
			prod_n *= n
			prod_d *= d
			
g = gcd(prod_n, prod_d)

print(f"ans = {prod_d // g}")