# Joe Tacheron
# run time: TIME

"""
999 Problem title

DETAILS

---
Solution Method

DETAILS
"""

import lib.num
from interface import Solution

class S999(Solution):

	def __init__(self):

		NUM  = 999
		NAME = "Problem title"
		ARG  = 1
		ANS  = 2
		
		super().__init__(NUM, NAME)
		self.add_test(ARG, ANS)
	
	def solve(self, arg):
	
################################################################################
	
		pass
		
################################################################################

if __name__ == "__main__":
	S999().run()