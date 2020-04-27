# Joe Tacheron
# Running time: instant

"""
106 Special subset sums: meta-testing

Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:

    S(B) ≠ S(C); that is, sums of subsets cannot be equal.
    If B contains more elements than C then S(B) > S(C).

For this problem we shall assume that a given set contains n strictly increasing elements and it already satisfies the second rule.

Surprisingly, out of the 25 possible subset pairs that can be obtained from a set for which n = 4, only 1 of these pairs need to be tested for equality (first rule). Similarly, when n = 7, only 70 out of the 966 subset pairs need to be tested.

For n = 12, how many of the 261625 subset pairs that can be obtained need to be tested for equality?

NOTE: This problem is related to Problem 103 and Problem 105.
"""

from lib.array import subsets
from interface import Solution

class S106(Solution):

	def __init__(self):

		NUM  = 106
		NAME = "Special subset sums: meta-testing"
		ARG  = 12
		ANS  = 21384
		
		super().__init__(NUM, NAME)
		self.add_test(4, 1)
		self.add_test(7, 70)
		self.add_test(ARG, ANS)
	
	def solve(self, length):
	
################################################################################

		def dominates(a, b):
			"""Given two sorted lists, return True if one list's elements are each larger than the corresponding element in the other list."""
			if all(a[i] < b[i] for i in range(len(a))):
				return True
			#if all(a[i] > b[i] for i in range(len(a))):
			#	return True
			return False

		arr = list(range(length))
		total = 0
		for s in subsets(arr, 2, len(arr)//2):
			s.sort() # not strictly needed given subsets' implementation
			
			complement = arr.copy()
			for a in s:
				complement.remove(a)
			
			for s2 in subsets(complement, len(s), len(s)):
				s2.sort()
				# first test below prevents checking all subset pairs twice
				if s[0] < s2[0] and not dominates(s, s2):
					total += 1
		return total#//2
		
################################################################################

if __name__ == "__main__":
	S106().run()