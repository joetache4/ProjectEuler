# Joe Tacheron
# Running time: instant

"""
113 Non-bouncy numbers

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

As n increases, the proportion of bouncy numbers below n increases such that there are only 12951 numbers below one-million that are not bouncy and only 277032 non-bouncy numbers below 10^10.

How many numbers below a googol (10100) are not bouncy?
"""

from interface import Solution

class S113(Solution):

	def __init__(self):

		NUM  = 113
		NAME = "Non-bouncy numbers"
		ARG  = 100 # power of 10
		ANS  = 51161058134250
		
		super().__init__(NUM, NAME)
		self.add_test(1, 9)
		self.add_test(2, 99)
		self.add_test(6, 12951)
		self.add_test(10, 277032)
		self.add_test(ARG, ANS)
	
	def solve(self, p):

		#last digit -> count increasing numbers
		inc = [1 for i in range(10)]
		inc[0] = 0
		#last digit -> count decreasing numbers
		dec = [1 for i in range(10)]
		dec[0] = 0
		
		nb = 9
		
		for length in range(p-1):
		
			for i in range(1,10):
				inc[i] += inc[i-1]
			for i in range(8,-1,-1):
				dec[i] += dec[i+1]
			
			nb += sum(inc)
			nb += sum(dec)		
			# discount repdigit numbers: both increasing and decreasing
			nb -= 9
			
		return nb

if __name__ == "__main__":
	S113().run()