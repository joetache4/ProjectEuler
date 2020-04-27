'''
It is possible to write ten as the sum of primes in exactly five different ways:

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over five thousand different ways?


ans: 71
'''


from lib.num import get_primes

primes = get_primes(10**3)

def c(n, start = 0, mem = {}):
	if n < 2 or primes[start] > n:
		return 0
	elif (n, start) in mem:
		return mem[(n, start)]
	else:
		ans = 1 if n in primes else 0
		for i in range(start, len(primes)):
			if primes[i] >= n:
				break
			ans += c(n-primes[i], i)
		mem[(n, start)] = ans
		return ans

for n in range(2, primes[-1]):
	if c(n) > 5000:
		print(n)
		break