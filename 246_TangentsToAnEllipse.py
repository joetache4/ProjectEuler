"""
A definition for an ellipse is:
Given a circle c with centre M and radius r and a point G such that d(G,M)<r, the locus of the points that are equidistant from c and G form an ellipse.
The construction of the points of the ellipse is shown below.

Given are the points M(-2000,1500) and G(8000,1500).
Given is also the circle c with centre M and radius 15000.
The locus of the points that are equidistant from G and c form an ellipse e.
From a point P outside e the two tangents t1 and t2 to the ellipse are drawn.
Let the points where t1 and t2 touch the ellipse be R and S.

For how many lattice points P is angle RPS greater than 45 degrees?

ans: 810834388
"""

"""
Solution method:

1.	Calculate angle for arbitrary point.
	
	Solve y(t)-Py / x(t)-Px  =  dy/dt / dx/dt  for t where x(t) and y(t) are the parametric equations for an ellipse. Eventually requires solving asin(t) + bcos(t) = c, which is done by dividing through by sqrt(a**2  +b**2). It becomes sin(B)sin(t) + cos(B)cos(t) = d  where B = atan(a/b). Use trig identity to get cos(t-B) = d  ->  t = +-acos(d) + atan(a/b) + 2n*pi.
	
	Use both t's to find tangent points. May need to add pi to a t if it's on the wrong side of the ellipse. Use law of cosines to get angle.

2.	Crawl around the grid marking a boundary where the angle is < 45deg.

3.	Count the size of this boundary

	The method to do this assumes the boundary is convex. It finds the difference between min and max heights of visited points in each column, and summing these differences. 

Notes:	

* equation for foci of ellipse: F**2 = M**2 - m**2  (F=dist from foci to center, M=semi-major axis, m=semi-minor axis)

* ellipse equation: (x/M)**2 + (y/m)**2 = 1

* parametric equation: x(t) = Mcos(t)  y(t) = msin(t)
"""

import math
from scipy.sparse import lil_matrix
import numpy as np
from lib.geom import Point

def cos_angle(p, major, minor):
	h  = math.sqrt((major*p.y)**2 + (minor*p.x)**2)
	a  = math.acos(major*minor/h)
	b  = 0
	
	if p.x == 0:
		if p.y > 0:
			b = math.pi / 2
		else:
			b = 3 * math.pi / 2
	else:
		b  = math.atan(major*p.y/minor/p.x)
		
	t1 =  a + b
	t2 = -a + b

	# there are two choices for each t, each opposite each other by pi radians
	# only one is the correct tangent line for this t
	# choose the one that's closest to p
	# an alternative (and much more complicated) method is to choose the one with the correct slope to p)
	
	tan = lambda t: Point(major * math.cos(t), minor * math.sin(t))
	
	tan1 = tan(t1)
	tmp  = tan(t1 + math.pi)
	if p.dist2(tmp) < p.dist2(tan1):
		tan1 = tmp
	
	tan2 = tan(t2)
	tmp  = tan(t2 + math.pi)
	if p.dist2(tmp) < p.dist2(tan2):
		tan2 = tmp
	
	a2 = p.dist2(tan1)
	b2 = p.dist2(tan2)
	c2 = tan1.dist2(tan2)
	a  = math.sqrt(a2)
	b  = math.sqrt(b2)
	
	return (a2 + b2 - c2) / (2 * a * b)

def more_than_45(major, minor):
	cos45 = math.cos(math.pi / 4)
	def mt45(p):
		return cos_angle(p, major, minor) < cos45
	return mt45

def ellipse(major, minor):
	return lambda p:(p.x)**2 / major**2 + (p.y)**2 / minor**2 <= 1

# creates a boundary where the outside region is where func is false
# returns the size of the bounded region
# NOTE: The size calculation is accurate only if the boundary is convex
def create_boundary(grid, func, start = None):
	#for judging interior size
	size = 0
	min_heights = {}
	max_heights = {}
	
	# for looking at adjacent squares
	moves = [(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1)]
	prev_move = 0
	
	# move as far to the left as posible
	if start is None:
		start = Point(0,0)
	p = start
	while func(p):
		p = p.left()
	p = p.right()
	start = p
	
	# continue moving until we're back where we started
	while True:		
		# make note of y-value of current column
		if p.x in min_heights:
			min_heights[p.x] = min(p.y, min_heights[p.x])
		else:
			min_heights[p.x] = p.y
		if p.x in max_heights:
			max_heights[p.x] = max(p.y, max_heights[p.x])
		else:
			max_heights[p.x] = p.y		
		# look at adjacent cells to move to
		look = (prev_move + 6) % 8 # ccw rotation 90deg
		for i in range(8):
			p_look = p.inc(moves[look])
			if grid[p_look.coord_centered(grid.shape)] == 0:
			#if grid[p_look.coord()] == 0:
				test = func(p_look)
				if test:
					# move
					p = p_look
					prev_move = look
					break
				else:
					# mark boundary
					grid[p_look.coord_centered(grid.shape)] = 1
					#grid[p_look.coord()] = 1
			look = (look + 1) % 8			
		if p == start:
			break
	
	# calculate size
	size = 0
	for key in min_heights:
		size = size + max_heights[key] - min_heights[key] + 1

	return size

################################################################################
# used for debugging

# count interior points
def brute_force_size(grid, start = None):
	if start is None:
		start = Point(0,0)
		
	size = 0
	
	base = start
	while grid[base.coord_centered(grid.shape)] == 0:
		p = base
		while grid[p.coord_centered(grid.shape)] == 0:
			size += 1
			p = p.up()
		base = base.right()
		
	base = start.left()
	while grid[base.coord_centered(grid.shape)] == 0:
		p = base
		while grid[p.coord_centered(grid.shape)] == 0:
			size += 1
			p = p.up()
		base = base.left()
		
	base = start.left().down()
	while grid[base.coord_centered(grid.shape)] == 0:
		p = base
		while grid[p.coord_centered(grid.shape)] == 0:
			size += 1
			p = p.down()
		base = base.left()
		
	base = start.down()
	while grid[base.coord_centered(grid.shape)] == 0:
		p = base
		while grid[p.coord_centered(grid.shape)] == 0:
			size += 1
			p = p.down()
		base = base.right()
	
	return size

def angle(p, major=1, minor=1):
	return(math.acos(cos_angle(p, major, minor)) / (2*math.pi) * 360)
	
# draw image 
def imshow(grid):
	import imageio
	import skimage.measure

	grid = grid.toarray()
	if max(grid.shape) > 10000:
		grid = skimage.measure.block_reduce(grid, (10,10), np.max)
	grid = 255 * grid
	imageio.imwrite("image.png", grid)

def test(major, minor):
	mt45 = more_than_45(major, minor)
	
	assert math.isclose(angle(Point(0,2)), 60)
	assert math.isclose(angle(Point(2,0)), 60)
	assert math.isclose(angle(Point(math.sqrt(2),math.sqrt(2))), 60)

	assert math.isclose(angle(Point(major, minor), major, minor), 90)
	assert math.isclose(angle(Point(-major, minor), major, minor), 90)
	assert math.isclose(angle(Point(major, -minor), major, minor), 90)
	assert math.isclose(angle(Point(-major, -minor), major, minor), 90)

	assert angle(Point(0, minor+1), major, minor) > 160	

	assert not mt45(Point(0, 6*major))
	assert not mt45(Point(6*major, 0))
	assert not mt45(Point(0, -6*major))
	assert not mt45(Point(-6*major, 0))

	assert not mt45(Point(6*major, 6*major))
	assert not mt45(Point(6*major, -6*major))
	assert not mt45(Point(-6*major, 6*major))
	assert not mt45(Point(-6*major, -6*major))	

	assert mt45(Point(0, major+1))
	assert mt45(Point(0, -major-1))
	assert mt45(Point(major+1, 0))
	assert mt45(Point(-major-1, 0))

	# assert angles increasing left to right above left half of ellipse
	angles = [angle(Point(m, minor+1), major, minor) for m in range(-major, 0, 1)]
	for i in range(1, len(angles)):
		assert angles[i] > angles[i-1]
		
	# assert angles decreasing going up
	angles = [angle(Point(0, minor+m), major, minor) for m in range(1, 100)]
	for i in range(1, len(angles)):
		assert angles[i] < angles[i-1]
	
	grid = lil_matrix((1000,1000), dtype = np.int8)
	assert create_boundary(grid, ellipse(major, minor)) == brute_force_size(grid)
	
	imshow(grid) # check manually

	print("tests complete")


#test(431, 237) # obvious error in imshow; no idea why
#test(430, 300) # slight error can be seen in imshow

################################################################################

radius = 15000
major  = radius//2
minor  = math.sqrt(major**2 - ((8000 - -2000)/2)**2)

grid = lil_matrix((3*radius,3*radius), dtype = np.int8)
num_mt45   = create_boundary(grid, more_than_45(major, minor), Point(-major-1,0))
num_inside = create_boundary(grid, ellipse(major, minor))
ans        = num_mt45 - num_inside
print(ans)
#imshow(grid)