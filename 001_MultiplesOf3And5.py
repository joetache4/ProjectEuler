# Joe Tacheron
# run time: instant

"""
001 Multiples of 3 and 5

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
"""

from interface import Solution

class S001(Solution):

	def __init__(self):

		NUM  = 1
		NAME = "Multiples of 3 and 5"
		ARG  = 1000 # test values below this
		ANS  = 233168

		super().__init__(NUM, NAME)
		self.add_test(ARG, ANS)
	
	def solve(self, upper):
		return sum(x for x in range(upper) if x%3 == 0 or x%5 == 0)

if __name__ == "__main__":
	S001().run()