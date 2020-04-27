"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

ans: 748317
"""

from lib.num import is_prime

# it is easy to generate all right-truncatable primes
# 2, 3, 5, and 7 are not included
def get_right_truncatable():
	primes = []
	for d in [2,3,5,7]:
		get_right_truncatable_r(d, primes)
	return primes

def get_right_truncatable_r(seed, primes):
	for d in [1,3,7,9]:
		num = 10 * seed + d
		if is_prime(num):
			primes.append(num)
			get_right_truncatable_r(num, primes)

# once the right-truncatable are generated,
# we then see which are left-truncatable
def is_left_truncatable_prime(p):
	if p % 10 in [0,1,4,6,8,9]:
		return False
	while p > 9:
		p = int(str(p)[1:])
		if not is_prime(p):
			return False
	return True

primes = get_right_truncatable()

assert len(primes) == 79

primes = [p for p in primes if is_left_truncatable_prime(p)]

assert len(primes) == 11

print(sum(primes))
