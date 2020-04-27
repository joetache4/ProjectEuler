"""
The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?

ans: 55
"""

from lib.num import get_primes

primes = get_primes(10**6)
primes = [p for p in primes if not any(d in str(p) for d in ["0","2","4","6","8"])]
primes.insert(0, 2)

def rotations(n):
	yield n
	m = n
	while True:
		m = str(m)
		m = int(m[1:] + m[0])
		if  m == n:
			break
		yield m

circular = []

for n in primes:
	is_circ = True
	for m in rotations(n):
		if m not in primes:
			is_circ = False
			break
	if is_circ:
		circular.append(n)

assert 2 in circular
assert 7 in circular
assert 11 in circular
assert 97 in circular
assert 23 not in circular
assert 47 not in circular

print(circular)
print(f"ans = {len(circular)}")