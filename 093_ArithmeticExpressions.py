"""
By using each of the digits from the set, {1, 2, 3, 4}, exactly once, and making use of the four arithmetic operations (+, −, *, /) and brackets/parentheses, it is possible to form different positive integer targets.

For example,

8 = (4 * (1 + 3)) / 2
14 = 4 * (3 + 1 / 2)
19 = 4 * (2 + 3) − 1
36 = 3 * 4 * (2 + 1)

Note that concatenations of the digits, like 12 + 34, are not allowed.

Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one different target numbers of which 36 is the maximum, and each of the numbers 1 to 28 can be obtained before encountering the first non-expressible number.

Find the set of four distinct digits, a < b < c < d, for which the longest set of consecutive positive integers, 1 to n, can be obtained, giving your answer as a string: abcd.


ans: 1258
"""

from lib.list import subsets

mem = {} # set of input values -> set of possible expression values

def get_vals(nums):
	try:
		return mem[tuple(sorted(nums))]
	except KeyError:
		ans = set()
		if len(nums) == 1:
			n = list(nums)[0]
			ans.add( n)
			ans.add(-n)
		else:
			for a in subsets(nums, min_size = 1, max_size = len(nums)-1):
				b = nums - a
				for x in get_vals(a):
					for y in get_vals(b):
						ans.add( x+y )
						ans.add( x-y )
						ans.add( x*y )
						try:
							ans.add( x/y ) # possible loss of precision
						except ZeroDivisionError:
							pass
		mem[tuple(sorted(nums))] = ans
		return ans

def count(s):
	exprs = sorted({ x for x in get_vals(s) if x == int(x) and x > 0 })
	for i in range(len(exprs)):
		if exprs[i] != i+1:
			return i
	return len(exprs)

ans = (-1, None)
for a in range(7):
	for b in range(a+1, 8):
		for c in range(b+1, 9):
			for d in range(c+1, 10):
				s = {a,b,c,d}
				ans = max( ans, (count(s),s) )

print("".join( str(d) for d in sorted(ans[1]) ))