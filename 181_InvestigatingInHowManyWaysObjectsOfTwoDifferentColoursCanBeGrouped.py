# Joe Tacheron
# run time: 133s

"""
181 Investigating in how many ways objects of two different colours can be grouped

Having three black objects B and one white object W they can be grouped in 7 ways like this:
(BBBW)	(B,BBW)	(B,B,BW)	(B,B,B,W) 	(B,BB,W)	(BBB,W)	(BB,BW)

In how many ways can sixty black objects B and forty white objects W be thus grouped?

---
Solution Method

This problem is identical to the partitioning of a multiset into sub-multisets, without regard to the order of sub-multisets or elements within sub-multisets.

Element order is disregarded by considering only the sum of elements in each sub-multiset. Sub-multiset order is disregarded by 'appending' them to the 'working list' in a sorted order.
"""

import lib.num
from interface import Solution

class S181(Solution):

	def __init__(self):

		NUM  = 181
		NAME = "Investigating in how many ways objects of two different colours can be grouped"
		ARG  = [60, 40] # black, white
		ANS  = 83735848679360680

		super().__init__(NUM, NAME)
		self.add_test([3,1], 7)
		self.add_test(ARG, ANS)
	
	def solve(self, amount):
	
		@lib.num.memoize
		def first_attempt(b, w, b_min = 0, w_min = 0):
			"""
			b, w = remaining black and white stones to place in groups.
			b_min, w_min = minimum such stones to place in each subsequent group.
			"""
			if b < 0 or w < 0:
				return 0
			if b == 0 and w == 0:
				return 1
			
			if w_min > w:
				b_min += 1
				w_min  = 0
			if b_min > b:
				return 0
			
			total = 0
			
			# same b, same or higher w
			b2 = b_min
			if b_min + w_min == 0:
				w_min = 1
			for w2 in range(w_min, w+1):
				total += first_attempt(b-b2, w-w2, b2, w2)
			
			# higher b, any w
			for b2 in range(b_min+1, b+1):
				for w2 in range(0, w+1):
					total += first_attempt(b-b2, w-w2, b2, w2)
			
			return total
			
		#return first_attempt(*amount)
	
		# time cant be cut in half by ignoring subproblems where b_min is too big.
		# when b_min is bigger than b/2, then there is only one solution, that with
		# all the black stones (and thus white ones, too) in the last group.
		# that option is also why 1 is added to the total in cases where b_min <= b//2.
		@lib.num.memoize
		def fast_solution(b, w, b_min = 0, w_min = 0):
			if b < 0 or w < 0:
				return 0
			if b == 0 and w == 0:
				return 1
			
			if w_min > w:
				b_min += 1
				w_min  = 0
			if b_min > b:
				return 0
			
			if b_min > b//2:
				return 1 # <--------------
				
			total = 0	
			
			# same b, same or higher w
			b2 = b_min
			if b_min == 0 and w_min == 0:
				w_min = 1
			for w2 in range(w_min, w+1):
				total += fast_solution(b-b2, w-w2, b2, w2)
			
			# higher b, any w
			for b2 in range(b_min+1, b//2+1): # <--------------
				for w2 in range(0, w+1):
					total += fast_solution(b-b2, w-w2, b2, w2)
			
			return total+1 # <--------------
			
		return fast_solution(*amount)
		
		# not mine
		def very_fast_solution(b, w):
			F = []
			for i in range(b+1):
				F.append([])
				for j in range(w+1):
					F[-1].append(0)

			F[0][0] = 1
			for i in range(b+1):
				for j in range(w+1):
					if i + j > 0:
						for k in range(i, b+1):
							for l in range(j, w+1):
								F[k][l] += F[k-i][l-j]

			return F[b][w]
			
		#return very_fast_solution(*amount)

if __name__ == "__main__":
	S181().run()