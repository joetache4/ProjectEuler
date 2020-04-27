"""
The decimal number, 585 = 1001001001 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)

ans: 872187
"""

from math import ceil

max = 10**6

def bits(n):
	bits = 0
	while n > 0:
		n = n >> 1
		bits += 1
	return bits

bits = bits(max)
palindromes = set()

def check(base2_str):
	n = int(base2_str, 2) # base-2 str -> decimal int
	# check if within bound
	if n < max:
		# check if palindrome
		if str(n) == str(n)[::-1]:
			palindromes.add(n)

# 10^6 has 20 digits (the largest 10 bit number is 2**10-1 = 1023)
# also, a base-2 palindrome must end in 1, meaning its odd
for n in range(1, 2**ceil(bits/2), 2):
	# create first half of binary 
	b = format(n, 'b')
	# mirror it
	a = b[::-1]
	# convert to decimal and check
	check(a[:-1] + b) # overlapping central bit
	for i in range(bits - len(b) - len(a) + 1): 
		check(a + "0"*i + b) # zeros added in middle

print(palindromes)
print(sum(palindromes))

def test(max):
	p = set()
	for n in range(1,max,2):
		b = format(n, 'b')
		if str(n) == str(n)[::-1] and b == b[::-1]:
			p.add(n)
	return sum(p)

# assert sum(palindromes) == test(max)