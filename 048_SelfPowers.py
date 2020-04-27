"""
Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.

ans: 9110846700
"""

from lib.num import mod_pow

num_digits = 10
upto = 1000

mod = 10**num_digits

def main(n):
	sum = 0
	for k in range(1, n+1):
		sum += mod_pow(k, k, mod)
	return sum % mod

def test():
	assert main(10) == 405071317
test()
	
print(main(upto))