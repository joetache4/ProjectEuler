"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?

ans: 7652413
"""

import sys
from lib.num import *

def pandigital(num):
	arr = [int(x) for x in str(num)]
	for k in range(1, len(arr)+1):
		if k not in arr:
			return False			
	return True;
	
# No 8- or 9-digit pandigital primes exist -- they fail divisibility-by-3 rule
max_val = 7654321

do_test = False
if len(sys.argv) > 1 and sys.argv[1] == "test":
	max_val = 87654321
	do_test = True
	print("Testing...")

primes = sieve_ero(max_val)

for i in range(max_val, 1, -1):
	if primes[i] and pandigital(i):
		if do_test: assert i == 7652413
		print(i)
		break
		
if do_test: print("[SUCCESS]")