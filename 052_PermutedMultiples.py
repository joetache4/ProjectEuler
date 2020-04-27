"""
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.

ans: 142857
"""

from lib.num import is_permutation as p

n = 1
while True:
	if all([ p(n, 2*n), p(n, 3*n), p(n, 4*n), p(n, 5*n), p(n, 6*n) ]):
		break
	n += 1
	
print(n)	
print(2*n)	
print(3*n)	
print(4*n)	
print(5*n)	
print(6*n)