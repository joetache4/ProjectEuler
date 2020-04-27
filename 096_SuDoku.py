"""
Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.

[puzzle grid and solution]

A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.

ans: 24702
"""

import copy
from _data.p096 import get_puzzles

class GuessNeededException(Exception):
	pass

class UnsolvableException(Exception):
	pass

class SolvedException(Exception):
	pass

# Some terminology I use in this file:
#
# terminology  example  definition
#
# allowables   [3,4,5]  numbers that may go into a cell without obvious error
# forced       [2]      when a cell has only one allowable - this input is "forced"
# input        [-6]     a number that has been "written down" into the puzzle
#                       it's negative so that it's not misidentified as a forced
# forbidden    []       no allowables - no input can go into this cell
#                       this indicates an error and the puzzle is unsolvable 
#                       in its current state

class Puzzle:

	# convert puzzle grid to grid of allowables
	def __init__(self, puzzle):
		self.allowables = []
		for row in range(9):
			self.allowables.append([])
			for col in range(9):
				self.allowables[row].append([x for x in range(1,10)])
		for row in range(9):
			for col in range(9):
				if puzzle[row][col] > 0:
					self.input(puzzle[row][col], row, col)

	# return true if all cells have input
	def solved(self):
		for row in range(9):
			for col in range(9):
				if len(self.allowables[row][col]) != 1 or self.allowables[row][col][0] > 0:
					return False
		return True

	# return true if the puzzle has no forbidden cells
	# (i.e., it appears solvable)
	def solvable(self):
		for row in range(9):
			for col in range(9):
				if len(self.allowables[row][col]) == 0:
					return False
		return True

	# find an input that is forced from the allowables
	# Or, raise SolvedException, UnsolvaleException, or GuessNeededException
	def scan(self):
		solved = True
		forced = None
		for row in range(9):
			for col in range(9):
				if len(self.allowables[row][col]) == 0:
					# any forbidden cells indicate an error with the current inputs
					raise UnsolvableException()
				elif len(self.allowables[row][col]) == 1:
					# might be a forced cell, might be an input
					if self.allowables[row][col][0] > 0:
						forced = (self.allowables[row][col][0], row, col) #return?
				else:
					# multiple choices means the puzzle is not yet solved
					solved = False
		if forced:
			return forced
		if solved:
			raise SolvedException()
		raise GuessNeededException()
	
	# update allowables when a new input is found
	def input(self, num, row, col):		
		for r in range(9):
			try:
				self.allowables[r][col].remove(num)
				#if r != row and len(self.allowables[r][col]) == 0: # this can be commented out
				#	raise UnsolvableException()
			except ValueError:
				pass
		for c in range(9):
			try:
				self.allowables[row][c].remove(num)
				#if c != col and len(self.allowables[row][c]) == 0:
				#	raise UnsolvableException()
			except ValueError:
				pass
		box_row = row // 3 * 3
		box_col = col // 3 * 3
		for r in range(box_row, box_row + 3):
			for c in range(box_col, box_col + 3):
				try:
					self.allowables[r][c].remove(num)
					#if r != row and c != col and len(self.allowables[r][c]) == 0:
					#	raise UnsolvableException()
				except ValueError:
					pass						
		self.allowables[row][col] = [-num] # negative indicates an input
		
	# input all numbers that are forced
	# until solved, unsolvable, or a guess is needed
	def reduce(self):
		try:
			while True:
				forced = self.scan()
				self.input(*forced)
		except GuessNeededException:
			pass
	
	# solve the puzzle
	# return a String representation of the solution
	def solve(self):
		try:
			self.solve_helper()
			#raise Exception("Solution not found")
			return "Puzzle not solved\n"
		except SolvedException:
			return str(self)

	# recursive helper function for solve
	def solve_helper(self):
		self.reduce()
		# make guesses
		for row in range(9):
			for col in range(9):
				choices = self.allowables[row][col]
				if len(choices) > 1:
					for choice in choices:
						allowables_old = copy.deepcopy(self.allowables)
						try:
							self.input(choice, row, col)
							self.solve_helper()
							assert False # should never get here - solve_helper always exits due to an exception
						except UnsolvableException:
							self.allowables = allowables_old
							self.allowables[row][col].remove(choice)
		raise UnsolvableException()

	def __str__(self):
		s = ""
		for row in range(9):
			for col in range(9):
				s += str(-self.allowables[row][col][0])
			s += "\n"
		return s
			
	def value(self):
		return 	100 * -self.allowables[0][0][0] + \
				 10 * -self.allowables[0][1][0] + \
				  1 * -self.allowables[0][2][0]

sum = 0
for p,i in zip(get_puzzles(), range(1, 51)):
	print(f"  Puzzle {i}")
	print()
	puzzle = Puzzle(p)
	sol = puzzle.solve()
	sum += puzzle.value()
	print(sol)
print(f"sum: {sum}")