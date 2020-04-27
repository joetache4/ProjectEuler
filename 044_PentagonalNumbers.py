"""
Pentagonal numbers are generated by the formula, Pn=n(3n−1)/2. The first ten pentagonal numbers are:

1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...

It can be seen that P4 + P7 = 22 + 70 = 92 = P8. However, their difference, 70 − 22 = 48, is not pentagonal.

Find the pair of pentagonal numbers, Pj and Pk, for which their sum and difference are pentagonal and D = |Pk − Pj| is minimised; what is the value of D?

ans: 5482660
"""

# brute force is probably not what was intended...

def get_pent_nums(max):
	n = 1
	while True:
		p = n * (3*n-1) // 2
		if p >= max:
			break
		yield p
		n += 1

pent_nums = list(get_pent_nums(10**7))

min = 999999999999999
for i in range(len(pent_nums)-1):
	for j in range(i+1, len(pent_nums)):
		p1 = pent_nums[i]
		p2 = pent_nums[j]
		if p1 + p2 in pent_nums and p2 - p1 in pent_nums:
			if p2 - p1 < min:
				min = p2 - p1
	
print(f"ans = {min}")