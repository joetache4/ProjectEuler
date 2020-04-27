# Joe Tacheron
# Running time: 5s

"""
112 Bouncy numbers

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand (525) are bouncy. In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time we reach 21780 the proportion of bouncy numbers is equal to 90%.

Find the least number for which the proportion of bouncy numbers is exactly 99%.
"""

from interface import Solution

class S112(Solution):

	def __init__(self):

		NUM  = 112
		NAME = "Bouncy numbers"
		ARG  = 0.99 # proportion bouncy
		ANS  = 1587000
		
		super().__init__(NUM, NAME)
		self.add_test(0.5, 538)
		self.add_test(0.9, 21780)
		self.add_test(ARG, ANS)
	
	def solve(self, p):
	
		def bouncy(n):
			if n < 100:
				return 0
			n = str(n)
			diff = [int(n[i]) - int(n[i+1]) for i in range(len(n)-1)]
			if min(diff) * max(diff) < 0:
				return 1
			else:
				return 0

		n = 1
		b = 0
		while b != n*p:
			n += 1
			b += bouncy(n)

		return n

if __name__ == "__main__":
	S112().run()