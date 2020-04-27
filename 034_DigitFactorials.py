"""
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: as 1! = 1 and 2! = 2 are not sums they are not included.

ans: 40730
"""

# After 1999999, numbers n are too large to be expressed as sum_fact_digits(n)
max = 19999999

f = {0:1, 1:1, 2:2, 3:6, 4:24, 5:120, 6:720, 7:5040, 8:40320, 9:362880}

def sum_fact_digits(n):
	return sum(f[int(d)] for d in str(n))

def find_nums():
	nums = []
	for n in range(10, max):
		if n == sum_fact_digits(n):
			nums.append(n)
	return nums

nums = find_nums()

print(nums)
print(f"ans = {sum(nums)}")