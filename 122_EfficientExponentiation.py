"""
The most naive way of computing n15 requires fourteen multiplications:

n × n × ... × n = n15

But using a "binary" method you can compute it in six multiplications:

n × n = n2
n2 × n2 = n4
n4 × n4 = n8
n8 × n4 = n12
n12 × n2 = n14
n14 × n = n15

However it is yet possible to compute it in only five multiplications:

n × n = n2
n2 × n = n3
n3 × n3 = n6
n6 × n6 = n12
n12 × n3 = n15

We shall define m(k) to be the minimum number of multiplications to compute nk; for example m(15) = 5.

For 1 ≤ k ≤ 200, find ∑ m(k).

ans: 1582
"""

n = 200

class Done(Exception):
	pass

def combine(exponents, max_depth, steps):
	if exponents[-1] > n or len(exponents) - 1 > max_depth:
		return
	
	try:
		steps[exponents[-1]] = min(steps[exponents[-1]], len(exponents)-1)
	except KeyError:
		steps[exponents[-1]] = len(exponents)-1
		if len(steps) == n:
			raise Done
	
	for i in range(len(exponents)):
		exp = exponents[i]
		exponents.append(exp + exponents[-1])
		combine(exponents, max_depth, steps)
		exponents.pop()

steps = {1:0}
try:
	for depth in range(n): # need to iterate depths in order to stop early in combine()
		combine([1], depth, steps)
		#print(f"{depth} {len(steps)}")
except Done:
	pass

#print(steps)
print(sum(( steps[k] for k in steps )))