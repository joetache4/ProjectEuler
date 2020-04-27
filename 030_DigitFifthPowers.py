"""
Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

    1634 = 14 + 64 + 34 + 44
    8208 = 84 + 24 + 04 + 84
    9474 = 94 + 44 + 74 + 44

As 1 = 14 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.

ans: 443839
"""

# Notice that sum_pow_digits(1,999,999) = 354,295 < 1,999,999
# Larger numbers continue this trend: they are too large for the sum of their digits
max = 1999999

def sum_pow_digits(n, pow = 5):
	return sum(int(d)**pow for d in str(n))

def find_nums_5():
	nums = []
	for n in range(2, max):
		if n == sum_pow_digits(n):
			nums.append(n)
	return nums

nums = find_nums_5()

print(nums)
print(f"ans = {sum(nums)}")