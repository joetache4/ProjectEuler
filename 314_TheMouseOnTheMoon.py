"""
The moon has been opened up, and land can be obtained for free, but there is a catch. You have to build a wall around the land that you stake out, and building a wall on the moon is expensive. Every country has been allotted a 500 m by 500 m square area, but they will possess only that area which they wall in. 251001 posts have been placed in a rectangular grid with 1 meter spacing. The wall must be a closed series of straight lines, each line running from post to post.

The bigger countries of course have built a 2000 m wall enclosing the entire 250 000 m2 area. The Duchy of Grand Fenwick, has a tighter budget, and has asked you (their Royal Programmer) to compute what shape would get best maximum enclosed-area/wall-length ratio.

You have done some preliminary calculations on a sheet of paper. For a 2000 meter wall enclosing the 250 000 m2 area the enclosed-area/wall-length ratio is 125.
Although not allowed , but to get an idea if this is anything better: if you place a circle inside the square area touching the four sides the area will be equal to π*2502 m2 and the perimeter will be π*500 m, so the enclosed-area/wall-length ratio will also be 125.

However, if you cut off from the square four triangles with sides 75 m, 75 m and 75√2 m the total area becomes 238750 m2 and the perimeter becomes 1400+300√2 m. So this gives an enclosed-area/wall-length ratio of 130.87, which is significantly better.
p314_landgrab.gif

Find the maximum enclosed-area/wall-length ratio.
Give your answer rounded to 8 places behind the decimal point in the form abc.defghijk.

ans: 132.52756426
"""


import math
from lib.progressbar import ProgressBar

r = 250 # radius

area = lambda x1, y1, x2, y2: abs(x1*y2 - x2*y1) / 2

dist = lambda x1, y1, x2, y2: math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# defines the optimal curve in the continuous case 
# found by solvng d(Ratio)/d(r_small) = 0
def rounded_corner_curve(x):
	r_small = 500/(2 + math.sqrt(math.pi))
	width_flat = r - r_small
	if x >= 0 and x <= width_flat:
		return r
	x_small = x - width_flat
	angle = math.acos(x_small / r_small)
	return width_flat + r_small * math.sin(angle)

# discrete answer is probably close to this curve
def close_to_curve(x, y, delta = 10):
	b = abs(y - rounded_corner_curve(x)) <= delta
	b = b or (x == r and y - rounded_corner_curve(x) <= delta)
	return b

est      = {(r,0):(0,0)}  # estimated increase to area and perim when the path is completed
prev     = {}             # used to reconstruct optimal path				
prev_ans = -1

while True: # loop until answer converges

	best = {(0,r):(0,0)}  # (dest.x, dest.y) -> (area, length) corresponding to best ratio
						  # of a path starting at (0,r) and going to (dest.x, dest.y)

	pb = ProgressBar(r)
	
	# loop each coordinate
	for x in range(r+1):
		
		pb.tick()
		
		for y in range(r, -1, -1):
			
			# don't go into circle
			if y*y + x*x < r*r:
				break
			if not close_to_curve(x, y):
				continue
			
			base_area, base_dist = best[(x, y)]
			
			# loop each neighbor
			# neighbors cannot be to the right or below
			for x2 in range(x, r+1):
				for y2 in range(y, -1, -1):
		
					if x2 == x and y2 == y:
						continue
						
					# don't go into circle
					if y2*y2 + x2*x2 < r*r:
						break
					if not close_to_curve(x2, y2):
						continue
					
					new_area = base_area + area(x, y, x2, y2)
					new_dist = base_dist + dist(x, y, x2, y2)
					
					est_area, est_dist = 0, 0
					try:
						est_area, est_dist = est[(x2, y2)] # using best[(y2, x2)] would fail
					except KeyError:
						pass
					
					# Try to find the best path by adding 
					# a/d of best path to [x,y]) + a/d to [x2, y2] + 
					# estimated a/d from [x2,y2] to [r,0].
					# Estimated a/d is 0,0 during first iteration.
					# Afterwards, estimated values comes from the 'best' list,
					# flipped across y=x.
					try:
						old_area, old_dist = best[(x2, y2)]
						
						if (new_area + est_area) * (old_dist + est_dist) > \
						   (new_dist + est_dist) * (old_area + est_area):
							best[(x2, y2)] = new_area, new_dist
							prev[(x2, y2)] = (x,y)
					except KeyError:
						best[(x2, y2)] = new_area, new_dist
						prev[(x2, y2)] = (x,y)

	# inspect answer
	a, d = best[(r,0)]
	ans = round(a / d, 8)
	print(ans)
	if ans == prev_ans:
		break
	prev_ans = ans
	est = {(c[1], c[0]):v for c,v in best.items()}

# inspect path
path = [(r,0)]
while path[0] != (0,r):
	path.insert(0, prev[path[0]])
nonlinear = lambda a,b,c: (a[0]-b[0]) * (a[1]-c[1]) != (a[0]-c[0]) * (a[1]-b[1])
path = [path[i] for i in range(len(path)) if i in [0, len(path)-1] or \
                                             nonlinear(path[i-1], path[i], path[i+1])]
print(path)



'''
import math 

def heron(a,b,c):
   s=(a+b+c)/2.
   v=s*(s-a)*(s-b)*(s-c)
   if v<0: return 0
   return math.sqrt(v)

def dist(x,y,x2,y2,r):
   a=math.sqrt(x**2+y**2)
   b=math.sqrt(x2**2+y2**2)
   c=math.sqrt((x-x2)**2+(y-y2)**2)
   A=heron(a,b,c)
   return A-r*c,A,c

W=250
def euler314(x,y,r,cache):
   key=(x,y)
   try:
      return cache[key]
   except KeyError:
      pass
   bests,besta,bestp=dist(x,y,y,x,r)
   bests*=0.5
   besta*=0.5
   bestp*=0.5   
   for y2 in range(y+1,min(y+15,W+1)):
      for x2 in range(y2,min(x+15,W+1)):
         s,a,p=dist(x,y,x2,y2,r)
         s2,a2,p2=euler314(x2,y2,r,cache)
         if s+s2>bests:
            bests,besta,bestp=s+s2,a+a2,p+p2
   cache[key]=(bests,besta,bestp)
   return bests,besta,bestp
oldratio=130.87
oldratio=132.526080628
#oldratio=132.527564257
s,a,p=euler314(250,0,oldratio,{})
print(s,a,p,a/p)
'''


# Graveyeard of failed attempts:

##########################################################################################################
# old utility functions

'''
def ratio(corners):
	a, d = 0, 0
	for i in range(len(corners) - 1):
		p1 = corners[i]
		p2 = corners[i+1]		
		d += dist(p1[0], p1[1], p2[0], p2[1])		
		# abs(a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y)) / 2 
		# a, b, c = p1, p2, (0, 0)
		a += area(p1[0], p1[1], p2[0], p2[1])
	return a / d

on_curve_upper = lambda x, y: y == math.ceil(rounded_corner_curve(x)) or \
                             (x == r and y <= math.ceil(rounded_corner_curve(r)))
on_curve_lower = lambda x, y: y == math.floor(rounded_corner_curve(x)) or \
                             (x == r and y <= math.floor(rounded_corner_curve(r)))

def imshow(path, file = "__path"):
	import imageio

	grid = [[0 for x in range(r+1)] for y in range(r+1)]
	for p in path:
		grid[r - p[0]][p[1]] = 255
	imageio.imwrite(file + ".png", grid)
'''

##########################################################################################################
# original DP algorithm here

'''
for x in range(r+1):
	for y in range(r, -1, -1):
		if y*y + x*x < r*r:
				break
		best[(x,y)] = (area(x,y,0,r), dist(x,y,0,r))
		prev[(x,y)] = (0,r)
		
# loop each coordinate, left to right
for x in range(1, r+1):
	
	pb.tick()
	
	for y in range(r, -1, -1):
		
		# don't go into circle
		if y*y + x*x < r*r:
			break
		
		# loop each neighbor - above and to the left this time
		for x2 in range(x+1):
			for y2 in range(r, y-1, -1):
					
				# don't go into circle
				if y2*y2 + x2*x2 < r*r:
					break
				if x == x2 and y == y2:
					continue
				
				dest_area, dest_dist = best[(x2, y2)]
								
				new_area = dest_area + area(x, y, x2, y2)
				new_dist = dest_dist + dist(x, y, x2, y2)
				
				old_area, old_dist = best[(x, y)]
				#  new_area / new_dist > old_area / old_dist:
				if new_area * old_dist > old_area * new_dist:
					best[(x, y)] = (new_area, new_dist)
					prev[(x, y)] = (x2, y2)
'''

##########################################################################################################
# genetic algorithm might work

# nudge each point to test for improvements
# loop while changes have led to improvements

'''
while True:
	changed = False
	old_ratio = ratio(path)
	print(old_ratio)
	
	# loop each corner (moving & deleting)
	i = 1
	while True:
		if i >= len(path)-1:
			break
		x = path[i][0]
		y = path[i][1]
		# loop test coordinates
		for y2 in range(path[i-1][1], path[i+1][1]-1, -1):
			for x2 in range(path[i-1][0], path[i+1][0]):
				path[i] = (x2, y2)
				new_ratio = ratio(path)
				if new_ratio > old_ratio:
					x = x2
					y = y2
					changed = True
					old_ratio = new_ratio
		path[i] = (x, y)
		if path[i] == path[i-1] or path[i] == path[i+1]:
			path.pop(i)
			i -= 1
		i += 1	
	
	if not changed:
		break
'''

##########################################################################################################
# select points close to a rounded curve
# 130.76617527

'''
from lib.point import Point

p = Point

def imshow(path, file = "__curve_path"):
	import imageio

	grid = [[0 for x in range(r+1)] for y in range(r+1)]
	for p in path:
		grid[r-p.y][p.x] = 255
	imageio.imwrite(file + ".png", grid)

def ratio(corners):
	length = 0
	area = 0
	
	for i in range(len(corners) - 1):
		p1 = corners[i]
		p2 = corners[i+1]
		
		length += p1.dist(p2)
		area += abs(p1.x*(p2.y-0) + p2.x*(0-p1.y)) / 2 
		
	return area / length

def concave(corners):
	prev_slope = 9999999
	for i in range(len(corners) - 1):
		slope = corners[i].slope(corners[i+1])
		if slope > prev_slope:
			return False
		prev_slope = slope
	return True

def midcurve(x):
	if x == 0:
		return r
	if x == r:
		return 0
	box_height = min(r, r * tan(acos(x/r)))
	circle_height = r * sin(acos(x/r))	
	return (box_height + circle_height) / 2
	
def rounded_corner(x):
	r_small = 500/(2 + math.sqrt(math.pi))
	width_flat = r - r_small
	if x >= 0 and x <= width_flat:
		return r
	x_small = x - width_flat
	angle = math.acos(x_small / r_small)
	return width_flat + r_small * math.sin(angle)

corners = []
for x in range(r + 1):
	corners.append(p(x, round(rounded_corner(x))))
corners.append(p(r, 0))
[print(c) for c in corners]
print(concave(corners))
print(ratio(corners))
'''

##########################################################################################################
# "pluck" corners that have a positive change in ratio or have a minimal negative change
# repeat until no more to pluck, see which was best

'''
from random import randint

# corners is a list of corners from bottom left to top right
# imagine a rubber band connecting the listed corners
# find how it would change if a corner is removed
# the first and last corner cannot be removed
# returns the number of added corners (NOT the same as the change in size
# as other corners may be removed)
def pluck(corners, index):
	if index <= 0 or index >= len(corners) - 1:
		raise ValueError
	
	plucked = corners.pop(index)
	
	cor_d = corners[index-1]
	cor_r = corners[index]
	adj_d = plucked.down()
	adj_r = plucked.right()
	
	on_a_line = lambda a, b, c: (b.y - a.y)*(c.x - a.x) == (b.x - a.x)*(c.y - a.y)
	
	new1, new2 = None, None
	
	#find new1
	candidates = [cor_r]
	if adj_d != cor_d                      \
	and not on_a_line(cor_d, adj_d, adj_r) \
	and not on_a_line(cor_d, adj_d, cor_r):
		candidates.append(adj_d)
	if  not on_a_line(cor_d, adj_r, cor_r):
		candidates.append(adj_r)
	
	new1 = min(candidates, key = lambda p: cor_d.angle(plucked, p))
	
	if new1 == cor_r:
		new1 = None
	
	#find new2
	candidates = [cor_d]
	if adj_r != cor_r                      \
	and not on_a_line(cor_r, adj_r, adj_d) \
	and not on_a_line(cor_r, adj_r, cor_d):
		candidates.append(adj_r)
	if  not on_a_line(cor_r, adj_d, cor_d):
		candidates.append(adj_d)
	
	new2 = min(candidates, key = lambda p: cor_r.angle(plucked, p))
	
	if new2 == cor_d:
		new2 = None
	
	# add to corners list
	added = 0
	if new1 is not None:
		corners.insert(index, new1)
		added += 1
	if new2 is not None and new2 != new1:
		corners.insert(index+1, new2)
		added += 1
	return added	

def undo_pluck(corners, plucked, index, remove):
	for i in range(remove):
		corners.pop(index)
	corners.insert(index, plucked)

def test_pluck():
	corners = [p(0,0), p(0,1), p(1,2), p(3,2)]
	i = 2
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 1
	assert corners == [p(0,0), p(0,1), p(2,2), p(3,2)]
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(0,1), p(1,2), p(3,2)]

	corners = [p(0,0), p(0,2), p(2,2)]
	i = 1
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 2
	assert corners == [p(0,0), p(0,1), p(1,2), p(2,2)]
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(0,2), p(2,2)]

	corners = [p(0,0), p(0,1), p(1,2), p(2,2)]
	i = 1
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 0
	assert corners == [p(0,0), p(1,2), p(2,2)]
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(0,1), p(1,2), p(2,2)]

	corners = [p(0,0), p(0,2), p(1,4), p(3,5), p(4,5)]
	i = 2
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 0
	assert corners == [p(0,0), p(0,2), p(3,5), p(4,5)]
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(0,2), p(1,4), p(3,5), p(4,5)]

	corners = [p(0,0), p(1,4), p(5,5)]
	i = 1
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 2
	assert corners == [p(0,0), p(1,3), p(2,4), p(5,5)]
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(1,4), p(5,5)]

	corners = [p(0,0), p(1,4), p(3,5)]
	i = 1
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 1
	assert corners == [p(0,0), p(1,3), p(3,5)]
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(1,4), p(3,5)]

	corners = [p(0,0), p(0, 250), p(250,250)]
	i = 1
	plucked = corners[i]
	r = pluck(corners, i)
	assert r == 2
	assert corners == [p(0,0), p(0,249), p(1,250), p(250,250)]
	assert ratio(corners) > 125
	undo_pluck(corners, plucked, i, r)
	assert corners == [p(0,0), p(0,250), p(250,250)]
		
	corners = [p(0,0), p(0,1), p(1,2), p(2,2)]
	undo_pluck(corners, p(0,2), 1, 2)
	assert corners == [p(0,0), p(0,2), p(2,2)]
test_pluck()

"""
c1 = [p(0,0),p(0,173),p(77, 250),p(250,250)]
r1 = ratio(c1)
from random import randint


import random
from datetime import datetime
random.seed(datetime.now())


best = c1
for i in range(10**5):
	a = randint(1,172)
	b = randint(1, 76)
	c2 = [p(0,0),p(0,a),p(b,173+b),p(77, 250),p(250,250)]
	r2 = ratio(c2)
	if r2 > r1:
		best = c2
		r1 = r2
[print(c) for c in best]
print(r1)
"""


def main(width):
	corners = [p(0, 0), p(0,width), p(width, width)]

	# keep pluckig corners until there is no improvement in ratio()
	prev_rat = ratio(corners)
	while True:
		changeMade = False
		
		# random start to see if solution depends on how we get there
		# if it does, then this method is wrong (answer should ne unique)
		length = len(corners)
		rand = randint(0, length-3)
		
		for i in range(1, length-1):
			i = (i - 1 + rand) % (length-2) + 1
			
			plucked = corners[i]
			rem = pluck(corners, i)
			rat = ratio(corners)
			if rat > prev_rat:
				#print(".", end="")
				prev_rat = rat
				changeMade = True
			else:
				undo_pluck(corners, plucked, i, rem)
		
		if not changeMade:
			break

	[print(c) for c in corners]
	ans = ratio(corners)
	print(f"exact = {ans}")
	print(f"ans   = {round(ans, 8)}")

main(width)
'''

##########################################################################################################
# loop all corners with some efficiencies - way too slow

'''
import math
from random import randint

mirror = lambda a: p(250 - a.y, 250 - a.x)

#on_a_line = lambda a, b, c: (b.y - a.y)*(c.x - a.x) == (b.x - a.x)*(c.y - a.y)
on_a_line = lambda a, b, c: math.isclose((b.y - a.y)*(c.x - a.x), (b.x - a.x)*(c.y - a.y))

inside_circle = lambda a: (a.x - 250)**2 + (a.y)**2 < 250**2

corners_key = lambda c: "".join((str(p) for p in c))

print_corners = lambda c: [print(p, end = "") for p in c]

print_ans = lambda a: print(round(a, 8))

area = lambda a, b, c: abs(a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y)) / 2 

def mirror_corners(corners):
	mir = corners.copy()
	for c in corners[::-1]:
		c2 = mirror(c)
		if c != c2:
			mir.append(c2)
	return mir

def inside_triangle(a, b, c, p):
	tri  = area(a, b, c)
	test = area(p, b, c) + area(a, p, c) + area(a, b, p)
	return math.isclose(test, tri)


# includes boundary
# not a general method, very specific to this program
def points_inside_triangle(a, b, c):
	for y in range(a.y + 1, math.floor(b.y) + 1):
		for x in range(a.x, math.floor(c.x) + 1):
			p1 = p(x, y)
			# this can be sped up by breaking when to the right of triangle
			# but this would be a lot less clear and more implementation-specific
			if inside_triangle(a, b, c, p1):
				yield p1

visited = set()
#best_ratio = 0
#best_corners = None

def check(corners, best):
	if randint(0, 200000) == 0:
		print_corners(best[1])
		print()
		print(best[0])
		#print("***")
		
	key = corners_key(corners)
	if key in visited:
		return
	visited.add(key)
	
	a = corners[-1]
	midpoint = a.midpoint(mirror(a))
	
	# calc ratio if the fence does not go into the circle
	if not inside_circle(midpoint):
		c = mirror_corners(corners)
		r = ratio(c)
		if r > best[0]:
			best[0] = r
			best[1] = c
		####
		#else:
		#	return
	
	# dont recurse if the last point is on the line y = -x + 250
	if a == midpoint:
		return
	
	# calc triangle points
	# a = last corner
	# b = intersection of y=-x+250 with line connecting corners[-1] and corners[-2]
	# c = midpoint (although it would be more efficient to use intersection of tangent 
	# line with y =-x+250)
	a = corners[-1]
	b = p(0, 250)
	try:
		if len(corners) > 1:
			# find intersection of slope with y = -x + 250
			c1 = corners[-1]
			c2 = corners[-2]
			m = c2.slope(c1)
			t = (250 - c1.x - c1.y) / (m + 1)
			b = Point(c1.x + t, c1.y + m*t)
			#assert on_a_line(corners[-1], corners[-2], b)
	except ZeroDivisionError:
		pass # vertical slope
	c = midpoint
	
	for p1 in points_inside_triangle(a, b, c):
		#####
		# continue if midpoint is inside circle
		# I didn't seriously think this would work but I tried it anyway
		#midpoint = p1.midpoint(mirror(p1))
		#if inside_circle(midpoint):
		#	continue
		#####
	
		if (len(corners) == 1 and p1.x == 0) or \
		(not inside_circle(p1) and not on_a_line(a, b, p1)):
		
			corners.append(p1)
			check(corners, best)
			corners.pop()

corners = [p(0,0)]
best    = [0, corners]
check(corners, best)
print_ans(best[0])
print_corners(best[1])
'''