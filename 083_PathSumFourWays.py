"""
NOTE: This problem is a significantly more challenging version of Problem 81.

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by moving left, right, up, and down, is indicated in bold red and is equal to 2297.

Find the minimal path sum from the top left to the bottom right by moving left, right, up, and down in matrix.txt (right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.

ans: 425185
"""

from queue import PriorityQueue
from _data.p083 import get_data

m = get_data()

test_m = [             \
[131,673,234,103, 18], \
[201, 96,342,965,150], \
[630,803,746,422,111], \
[537,699,497,121,956], \
[805,732,524, 37,331]]

def dijkstras(m):
	q = PriorityQueue()
	visited = set()

	q.put((m[0][0], 0, 0))

	height = len(m)
	width = len(m[0])

	while not q.empty():
		cost, x, y = q.get()
		
		if (x, y) == (width-1, height-1):
			return cost

		if (x, y) in visited:
			continue
		visited.add((x, y))
		
		if x < width - 1:
			q.put((cost + m[x + 1][y], x + 1, y))
		if x > 0:
			q.put((cost + m[x - 1][y], x - 1, y))
		if y < height - 1:
			q.put((cost + m[x][y + 1], x, y + 1))
		if y > 0:
			q.put((cost + m[x][y - 1], x, y - 1))
	
	return -1

test = dijkstras(test_m)
print(test)
assert test == 2297

print(dijkstras(m))