"""
An irrational decimal fraction is created by concatenating the positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value of the following expression.

d1 × d10 × d100 × d1000 × d10000 × d100000 × d1000000

ans: 210
"""

import sys

do_test = False

if len(sys.argv) > 1 and sys.argv[1] == "test":
	do_test = True

def d(n):
	# get digit count of number that contains n-th digit
	len = 10
	digit_count = 1
	while len <= n:
		n -= len # set n to an index that ignores shorter numbers
		digit_count += 1
		len = digit_count * 9 * 10**(digit_count-1)
	# get the number at this index
	num = n // digit_count
	if digit_count > 1:
		num += 10**(digit_count - 1)
	# get the digit
	dig = int(str(num)[n % digit_count])
	return dig

def test():
	print("Testing...")
	concatted = [str(x) for x in range(100000)]
	concatted = "".join(concatted)
	for i in range(1,10000):
		assert d(i) == int(concatted[i])
	print("[SUCCESS]")

if do_test:
	test()
else:
	ans = d(1) * d(10) * d(100) * d(1000) * d(10000) * d(100000) * d(1000000)
	print(ans)