import sys
import os

class _UnexpectedResultError(Exception):
	"""Indicates a mismatch between return value and expected value."""
	pass

class Solution:
	def __init__(self, num, name):
		self.num = num
		self.name = name
		self.tests = []
	
	def add_test(self, args, ans = None):
		"""Add an argument-answer pair to the test queue."""
		self.tests.append((args, ans))
	
	def solve(self, args):
		"""The solution algorithm implemented by subclasses."""
		raise NotImplementedError()
	
	def test(self):
		"""Any additional tests."""
		pass
	
	def run(self):
		"""Run all tests, check results (if able), and print."""
		try:
			self.test()
			for args, ans in self.tests:
				val = self.solve(args)
				if ans is not None and str(val) != str(ans):
					info = [f"Unexpected Result: solve({args})", f"Expected: {ans}", f"     Got: {val}"]
					raise _UnexpectedResultError("\n".join(info))
				print(f"solve({args}) {'==' if ans else '~ '} {val}")
		except KeyboardInterrupt:
			raise KeyboardInterrupt() from None # deletes old stack trace
		except _UnexpectedResultError as e:
			print(e)
			sys.exit(1)