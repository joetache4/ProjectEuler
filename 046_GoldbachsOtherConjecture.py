"""
Problem 46 at ProjectEuler.net

Find the smallest odd composite number that cannot 
be written as the sum of a prime and twice a square

ans: 5777
"""

from lib.num import is_prime

# if target is the sum of prime + 2*k^2, return k
# otherwise return -1
def try_solve(target, prime):
	k = 1
	while True:
		sum = prime + 2 * k * k
		if sum == target:
			return k
		elif sum > target:
			return -1
		k += 1
	raise Exception()

def main():
	n = 9
	while True:
		succeed = False
		for p in range(n):
			if not is_prime(p):
				continue
			#print("*{}".format(p))
			k = try_solve(n, p)
			if k > 0:
				#print("{} = {} + 2 * {}^2".format(n, p, k))
				succeed = True
				break
		if not succeed:
			print(n)
			break
		# set n to next odd composite number
		n += 2
		while is_prime(n):
			n += 2
				
main()