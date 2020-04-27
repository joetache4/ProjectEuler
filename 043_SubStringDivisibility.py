"""
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

    d2d3d4=406 is divisible by 2
    d3d4d5=063 is divisible by 3
    d4d5d6=635 is divisible by 5
    d5d6d7=357 is divisible by 7
    d6d7d8=572 is divisible by 11
    d7d8d9=728 is divisible by 13
    d8d9d10=289 is divisible by 17

Find the sum of all 0 to 9 pandigital numbers with this property.

ans: 16695334890
"""

import sys

# a b c d e f g h i j
# 1 2 3 4 5 6 7 8 9 10

do_test = len(sys.argv) > 1 and sys.argv[1] == "test"

def num(*dig):
	return int(''.join([str(x) for x in dig]))
	
nums = []

for a in range(10):
	for b in range(10):
		if a == b: continue
		for c in range(10):
			if c in [a,b]: continue
			for d in [0, 2, 4, 6, 8]:
				if d in [a,b,c]: continue
				for e in range(10):
					if e in [a,b,c,d]: continue
					if (c+d+e)%3 != 0: continue
					for f in [0, 5]:
						if f in [a,b,c,d, e]: continue
						for g in range(10):
							if g in [a,b,c,d,e,f]: continue
							#if (10*e + f - 2*g) % 7 != 0: continue
							if (100*e + 10*f + g) % 7 != 0: continue
							for h in range(10):
								if h in [a,b,c,d,e,f,g]: continue
								if (100*f + 10*g + h) % 11 != 0: continue
								for i in range(10):
									if i in [a,b,c,d,e,f,g,h]: continue
									if (100*g + 10*h + i) % 13 != 0: continue
									for j in range(10):
										if j in [a,b,c,d,e,f,g,h,i]: continue
										if (100*h + 10*i + j) % 17 != 0: continue
										n = num(a,b,c,d,e,f,g,h,i,j)
										nums.append(n)
										
if do_test:
	print("Testing...")
	assert 1406357289 in nums
	print("[SUCCESS]")
else:
	for n in nums:
		print(n)
	print("sum: {}".format(sum(nums)))