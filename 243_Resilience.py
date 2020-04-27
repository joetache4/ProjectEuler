"""
A positive fraction whose numerator is less than its denominator is called a proper fraction.
For any denominator, d, there will be d−1 proper fractions; for example, with d = 12:
1/12 , 2/12 , 3/12 , 4/12 , 5/12 , 6/12 , 7/12 , 8/12 , 9/12 , 10/12 , 11/12 .

We shall call a fraction that cannot be cancelled down a resilient fraction.
Furthermore we shall define the resilience of a denominator, R(d), to be the ratio of its proper fractions that are resilient; for example, R(12) = 4/11 .
In fact, d=12 is the smallest denominator having a resilience R(d) < 4/10 .

Find the smallest denominator d, having a resilience R(d) < target .

ans: 892371480
"""

from lib.num import get_primes

primes = get_primes(10**6)

target = 15499/94744

# from simply adding more primes to reduce R(d), upper bound is 6_469_693_230
# which is the product of: 2,3,5,7,11,13,17,19,23,29

prod = 1
d = 1
for p in primes:
	prod *= (1 - 1/p)
	d *= p
	print(f"{p} d={d}, resilience={d*prod/(d-1)}")
	if d*prod/(d-1) < target: break 
print()

# Also, by manipulating the inequality R(d) < target, it must be that 
# Prod{1-1/p, primes p} < target. So a lower bound for d is 223_092_870
# which is the product of: 2,3,5,7,11,13,17,19,23

prod = 1
d = 1
for p in primes:
	prod *= (1 - 1/p)
	d *= p
	print(f"{p} d={d}, tot(d)/d={prod}")
	if prod < target: break 
print()

# Now, take d = 223_092_870 and keep multiplying by 2 until R(d) < target.

count = 0
while d*prod/(d-1) >= target:
	d *= 2
	count += 1
print(f"223092870 * 2^{count} = {d}, R(d) < target")
print()

# Result: 223_092_870 * 2^2 = 892_371_480. 
# We now just need to check R(d) by multiplying all combinations of primes 
# s.t. the prime-product is < 2^2. The only other option, then, is 3. 
# So, check if R(223092870 * 3) < target.

d = 223_092_870 * 3
if d*prod/(d-1) >= target:
	d = 892_371_480
print(f"ans: {d}")