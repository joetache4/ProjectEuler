"""
Take the number 192 and multiply it by each of 1, 2, and 3:

    192 × 1 = 192
    192 × 2 = 384
    192 × 3 = 576

By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?

ans: 9327 * ([0, 1, 2]) = 932718654
"""

def pandigital(num):
	if num < 123456789 or num > 987654321:
		return False
		
	arr = [int(x) for x in str(num)]
	for k in range(1, 10):
		if k not in arr:
			return False
			
	return True
	
def concat(k, n):
	arr = [str(k*m) for m in range(1, n+1)]
	s = ''.join(arr)
	return int(s)

class Solution:
	def __init__(self):
		#self.best_k = 9
		#self.best_n = 5
		#self.max = 918273645	
		self.best_k = -1
		self.best_n = -1
		self.max = -1	

	def try_find(self, k_max, n):
		for k in range(1, k_max+1):
			prod = concat(k, n)
			if prod > self.max and pandigital(prod):
				self.max = prod
				self.best_k = k
				self.best_n = n	
		return self
				
def test():
	assert pandigital(123456789)
	assert pandigital(987654321)
	assert pandigital(582691374)
	assert not pandigital(0)
	assert not pandigital(192365984)
	assert not pandigital(12345986)
	
	assert concat(9, 5) == 918273645
	assert concat(9, 4) == 9182736
	assert concat(1, 9) == 123456789
	
	assert pandigital(concat(9, 5))
	
	assert Solution().try_find(1, 9).max == 123456789
	assert Solution().try_find(9, 5).max == 918273645
test()

solution = Solution()

# For clarity, let len(k * 1 to n) mean len(concat(k, n))

# n = 2
# k <= 9999
# reason: if k had 5 digits, then k concatted with 2k has 10 digits
# this isn't a problem if k has 4 digits
solution.try_find(9999, 2)
# n = 3
# k <= 333
#reason: if k==334, then len(334 * 1to3) has 3+3+4 digits
# this isn't a problem when k==333
solution.try_find(333, 3)
# n = 4
# k <= 33
#reason: if k==34, then len(34 * 1to4) has 2+2+3+3 digits
# this isn't a problem when k==33
solution.try_find(33, 4)
# n = 5
# k <= 9
#reason: if k==10, then len(10 * 1to5) has 2*5 digits
# this isn't a problem when k==9
solution.try_find(9, 5)
# n = 6
# k <= 2
#reason: if k==4, then len(4 * 1to6) has 1+1+2+2+2+2 digits
# this isn't a problem when k==3
solution.try_find(3, 6)
# n = 7
# k <= 1
#reason: if k==2, then len(2 * 1to7) has 1+1+1+1+2+2+2 digits
# this isn't a problem when k==1
solution.try_find(1, 7)
# n = 8
# k <= 1
#reason: if k==2, then len(2 * 1to8) has 1+1+1+1+2+2+2+2 digits
# this isn't a problem when k==1
solution.try_find(1, 8)
# n = 9
# k <= 1
#reason: if k==2, then len(2 * 1to9) has 1+1+1+1+2+2+2+2+2 digits
# this isn't a problem when k==1
solution.try_find(1, 9)
# n cannot be more than 9, because then even k==1 will be too much
# However, k can't be zero or negative, either. So, no k works.

assert pandigital(solution.max)

print("{} * ({}) = {}".format(
	solution.best_k, 
	[x for x in range(solution.best_n+1)], 
	solution.max))