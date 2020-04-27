"""
The Fibonacci sequence is defined by the recurrence relation:

    Fn = Fn−1 + Fn−2, where F1 = 1 and F2 = 1.

It turns out that F541, which contains 113 digits, is the first Fibonacci number for which the last nine digits are 1-9 pandigital (contain all the digits 1 to 9, but not necessarily in order). And F2749, which contains 575 digits, is the first Fibonacci number for which the first nine digits are 1-9 pandigital.

Given that Fk is the first Fibonacci number for which the first nine digits AND the last nine digits are 1-9 pandigital, find k.


ans: 329468
"""

from decimal import Decimal as D

def pandigital(s):
	return all(( str(i) in s for i in range(1, 10) ))

def fib(mod, mem = [1, 0, 1]): # index (n), F_n-1, F_n
	while True:
		yield mem[0], mem[2]
		mem[0], mem[1], mem[2] = mem[0] + 1, mem[2], (mem[1] + mem[2]) % mod

def fib_pan_last():
	for i, f in fib(10**9):
		if pandigital(str(f)):
			yield i

phi = D('1.618033988749894848204586834365638117720309179805762862135')
rt5 = D('2.236067977499789696409173668731276235440618359611525724270')

for n in fib_pan_last():
	f = phi**n 
	f = f - (-phi)**(-n)
	f = f / rt5
	if pandigital(str(f)[:10]):
		print(n)
		break