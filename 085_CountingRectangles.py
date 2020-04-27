"""
By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains eighteen rectangles:

Although there exists no rectangular grid that contains exactly two million rectangles, find the area of the grid with the nearest solution.

ans: 2772
"""

import math

# Counts the total number of bars in a grid.
def count_rect(height, width):
	sum = 0
	# 1 x 1
	sum += height * width
	# 1 x n
	sum += height * width * (width-1) // 2
	# n x 1
	sum += width * height * (height-1) // 2
	# m x n
	sum += height * (height-1) // 2 * width * (width-1) // 2
	return sum

def find_min_diff(area, target = 2*10**6):
	min_diff = -1
	closest = None
	max_width = int(math.sqrt(area))
	for width in range(1, max_width+1):
		if area % width == 0:
			rect = count_rect(area//width, width)
			diff = abs(target - rect)			
			if min_diff == -1 or diff < min_diff:
				min_diff = diff
				closest = (diff, area//width, width)
	return closest

closest = min( (find_min_diff(a) for a in range(1, 2*10**6)) )
print(f"area = {closest[1]*closest[2]}")