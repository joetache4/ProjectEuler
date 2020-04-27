"""
Given is the arithmetic-geometric sequence u(k) = (900-3k)r^(k-1).
Let s(n) = Σk=1...n u(k).

Find the value of r for which s(5000) = -600,000,000,000.

Give your answer rounded to 12 places behind the decimal point.


ans: 1.002322108633
"""

# Just increment digits one at a time and keep the highest
# that keeps the result above -6*10**11

import decimal
D = decimal.Decimal

c = -6*10**11

def u(k, r):
	return (900-3*k)*r**(k-1)

def s(r, n = 5000):
	return sum(( u(k, r) for k in range(1, n+1) ))


base = "1." # easy to see r is between between 1 and 2
for digit_index in range(13):
	best_val = 0
	for val in range(10):
		num = D(base + str(val))
		if s(num) >= c:
			best_val = val
		else:
			break
	base = base + str(best_val)
	print(base)
	
print(f"ans = {round(D(base), 12)}")
print(f"s({base}) = {s(D(base))}")
	


# Newton's Method does not converge
'''
def du(k, r):
	return (900-3*k)*(k-1)*r**(k-2)
	
def ds(r, n = 5000):
	return sum(( du(k, r) for k in range(2, n+1) ))
	
rn = 1.001
for i in range(100):
	rn = rn - s(rn)/ds(rn)
	#print(s(rn) - c)
print(s(rn))
'''

