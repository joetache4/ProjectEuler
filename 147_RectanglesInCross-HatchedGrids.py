"""
In a 3x2 cross-hatched grid, a total of 37 different rectangles could be situated within that grid as indicated in the sketch.

There are 5 grids smaller than 3x2, vertical and horizontal dimensions being important, i.e. 1x1, 2x1, 3x1, 1x2 and 2x2. If each of them is cross-hatched, the following number of different rectangles could be situated within those smaller grids:
1x1	1
2x1	4
3x1	8
1x2	4
2x2	18

Adding those to the 37 of the 3x2 grid, a total of 72 different rectangles could be situated within 3x2 and smaller grids.

How many different rectangles could be situated within 47x43 and smaller grids?

ans: 846910284
"""

M = 47 # height
N = 43 # width

# "diamond" = any diagonal rectangle, "bar" = any horizontal or vertical rectangle

# Return True if a diamond with the given leftmost and rightmost coordinates 
# will fit inside a grid of the given height and width AND if the bounds do not 
# extend beyond the coordinates left/right. Return False otherwise.
# Coordinates are from top left corner, x to right, y down.
# Coordinates go by increments of 0.5.
def bounded_diamond(height, width, x1, y1, x2, y2):
	if abs(x1 - x2) == abs(y1 - y2): # on y=x or y=-x line
		return False
	
	# solve system of equations to get diamonds bounds
	t = (x2 - y2 - x1 + y1) / 2	
	x3, y3 = x1 + t, y1 - t
	# the first 4 check if out of bounds; the last two check if the diamond has a different actual start/end point
	if x3 < 0 or y3 < 0 or x3 > width or y3 > height or x3 < x1 or x3 > x2: 
		return False		
	x3, y3 = x2 - t, y2 + t
	if x3 < 0 or y3 < 0 or x3 > width or y3 > height or x3 < x1 or x3 > x2:
		return False
	
	return True

# Counts the number of diamonds that have left and right corners 
# in the leftmost and rightmost cells of the grid.
mem = {}
def count_spanning_diamonds(height, width):
	if width >= height + 2:
		# too wide for anything
		return 0
	
	if width == 1:
		return height - 1		
	
	if (height, width) in mem:
		return mem[(height, width)]
	
	count = 0
	x1 = 0.5
	y1 = 0.5
	for i in range(1, 2*height):
		
		x2 = width - 0.5
		y2 = 0.5
		for j in range(1, 2*height):
			if bounded_diamond(height, width, x1, y1, x2, y2):
				count += 1
			
			if x2 == width:
				x2 -= 0.5
			else:
				x2 = width
			y2 += 0.5
			
		x1 = (x1 + 0.5) % 1
		y1 += 0.5
	
	mem[(height, width)] = count
	return count

# Counts the total number of diamonds in a grid.
def count_diamonds(height, width):	
	sum = 0
	for w in range(1, width+1):
		sum += (width - w + 1) * count_spanning_diamonds(height, w)
	return sum

# Counts the total number of bars in a grid.
def count_bars(height, width):
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

total = 0
for h in range(1, M + 1):
	for w in range(1, N + 1):
		total += count_bars(h, w)
		total += count_diamonds(h, w)
print(total)