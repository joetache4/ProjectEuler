"""
By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family.


ans: 121313
"""

from collections import Counter
from lib.num import binary_search
from _data._primes import get_data

primes = get_data()

length = 0

lo = -1
hi = 0

while True:
	# Look at primes in batches of equal length.
	length += 1
	lo = hi
	hi = lo + 1
	while primes[hi] < 10**length:
		hi += 1
	
	# replace digits 0-9 with 'x' and count occurrences
	total = Counter()
	for d in range(10):
		replaced = Counter([str(x).replace(str(d), "x") for x in primes[lo:hi]])
		for k in replaced:
			if "x" in k:
				total[k] += replaced[k]
	
	# Above method will undercount occurrences.
	# e.g., 56333/3  -->  56xxx  but it should also be counted as part of the 56xx3 template.
	# So, for each template, replace 'x' with digits already in the template
	# and see if the result is prime.
	for k, v in total.items():
		not_replaced = {d for d in k}
		not_replaced.remove("x")
		if len(not_replaced) + v < 8:
			continue # not possible so don't try
		for r in not_replaced:
			if binary_search(primes[lo:hi], int(k.replace("x",r))) != -1:
				total[k] += 1
	
	# Get templates of 8-family primes.
	templates = set()
	for k in total:
		if total[k] == 8:
			templates.add(k)
	
	# Find smallest prime that's part of one of these tempaltes.
	if len(templates) > 0:
		p = set()
		for t in templates:
			# For an 8-family, there must be a prime after replacing with 0, 1, or 2.
			a = int(t.replace("x","0"))
			if binary_search(primes[lo:hi], a) and t[0] != "x":
				p.add(a)
			a = int(t.replace("x","1"))
			if binary_search(primes[lo:hi], a):
				p.add(a)
			a = int(t.replace("x","2"))
			if binary_search(primes[lo:hi], a):
				p.add(a)
		print(min(p))
		break
		