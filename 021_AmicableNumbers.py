"""
Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.

ans: 31626
"""

from lib.num import divisors

max = 10000

memory = {}
def d(num):
	if num <= 0:
		return num
	elif num == 1:
		return -0.5
	elif num in memory:
		return memory[num]
	else:
		div = divisors(num)
		sum = 0
		for n in div:
			sum += n
		sum -= num
		memory[num] = sum
		return sum

assert d(220) == 284
assert d(284) == 220

amicable = set()
for n in range(1, max+1):
	sum = d(n)
	if sum != n and d(sum) == n:
		print("amicable: {}, {}".format(n, sum))
		amicable.add(n)
		amicable.add(sum)

#print(amicable)

sum = 0
for n in amicable:
	sum += n
print("sum: {}".format(sum))