"""
n! means n × (n − 1) × ... × 3 × 2 × 1

For example, 10! = 10 × 9 × ... × 3 × 2 × 1 = 3628800,
and the sum of the digits in the number 10! is 3 + 6 + 2 + 8 + 8 + 0 + 0 = 27.

Find the sum of the digits in the number 100!

ans: 648
"""

from lib.num import factorial

def main(n):
	num = factorial(n)
	sum = 0
	for d in str(num):
		sum += int(d)
	return sum
	
assert main(10) == 27
	
print(main(100))