"""
In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by only moving to the right and down, is indicated in bold red and is equal to 2427.

[grid]

Find the minimal path sum, in matrix.txt (right click and "Save Link/Target As..."), a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by only moving right and down.

ans: 427337
"""

from _data.p081 import get_data

# need to be able to access numbers by reference, not value
class Cell:
	def __init__(self, val):
		self.value  = val
		self.bottom = None
		self.right  = None
		self.min    = None
	
	# recursively finds minimum path
	def get_min(self):
		if self.min is not None:
			return self.min
		else:
			if self.bottom is None:
				self.min = self.value + self.right.get_min()
				return self.min
			elif self.right is None:
				self.min = self.value + self.bottom.get_min()
				return self.min
			self.min = self.value + min(self.bottom.get_min(), self.right.get_min())
			return self.min
	
data = get_data()
# convert primitive numbers into Cells
for i in range(len(data)):
	for j in range(len(data[i])):
		data[i][j] = Cell(data[i][j])
# set bottom and right relationships
for i in range(len(data)):
	for j in range(len(data[i])):
		try:
			data[i][j].bottom = data[i+1][j]
		except:
			pass
		try:
			data[i][j].right = data[i][j+1]
		except:
			pass
			
# bottom-right Cell is the only one to not have bottom or right children,
# has to be given special attention
data[-1][-1].min = data[-1][-1].value
print(data[0][0].get_min())