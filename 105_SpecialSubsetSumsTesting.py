# Joe Tacheron
# Running time: instant

"""
105 Special subset sums: testing

Let S(A) represent the sum of elements in set A of size n. We shall call it a special sum set if for any two non-empty disjoint subsets, B and C, the following properties are true:

    S(B) ≠ S(C); that is, sums of subsets cannot be equal.
    If B contains more elements than C then S(B) > S(C).

For example, {81, 88, 75, 42, 87, 84, 86, 65} is not a special sum set because 65 + 87 + 88 = 75 + 81 + 84, whereas {157, 150, 164, 119, 79, 159, 161, 139, 158} satisfies both rules for all possible subset pair combinations and S(A) = 1286.

Using sets.txt (right click and "Save Link/Target As..."), a 4K text file with one-hundred sets containing seven to twelve elements (the two examples given above are the first two sets in the file), identify all the special sum sets, A1, A2, ..., Ak, and find the value of S(A1) + S(A2) + ... + S(Ak).

NOTE: This problem is related to Problem 103 and Problem 106.
"""

from lib.array import subsets
from data.p105 import get_data
from interface import Solution

class S105(Solution):

	def __init__(self):

		NUM  = 105
		NAME = "Special subset sums: testing"
		ARG  = None
		ANS  = 73702
		
		super().__init__(NUM, NAME)
		self.add_test(ARG, ANS)
	
################################################################################

	def cond1(self, arr):
		sums = set()
		for subset in subsets(arr):
			s = sum(subset)
			if s in sums:
				return False
			sums.add(s)
		return True

	def cond2(self, arr):
		arr.sort()
		m = arr[0] # sum of lower terms
		M = 0      # sum of higher terms
		a = 1
		b = len(arr)-1
		while a < b:
			m += arr[a]
			M += arr[b]
			if m <= M:
				return False
			a += 1
			b -= 1
		return True
	
	def solve(self, arg):
		total = 0
		for arr in get_data():
			if self.cond2(arr) and self.cond1(arr):
				total += sum(arr)
		return total
	
	def test(self):
		assert not self.cond1([81, 88, 75, 42, 87, 84, 86, 65])
		assert self.cond1([157, 150, 164, 119, 79, 159, 161, 139, 158])
		assert self.cond2([157, 150, 164, 119, 79, 159, 161, 139, 158])
		
################################################################################

if __name__ == "__main__":
	S105().run()
