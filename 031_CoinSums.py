"""
In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

It is possible to make £2 in the following way:

    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?

ans: 73682
"""

def ways(amount, nohigher=200):
	if amount == 0:
		return 1
	
	count = 0	
	coins = [1, 2, 5, 10, 20, 50, 100, 200]
	
	for c in coins:
		if amount >= c and c <= nohigher:
			count += ways(amount - c, c)
	
	return count

print(ways(200))