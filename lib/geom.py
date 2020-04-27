from math import sqrt, acos

from lib.array import cmp_to_key

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def dist(self, other):
		return sqrt(self.dist2(other))
	
	def dist2(self, other):
		return (self.x - other.x)**2 + (self.y - other.y)**2
	
	def slope(self, other):
		return (other.y - self.y) / (other.x - self.x)
	
	def angle(self, p1, p2):
		a = self.dist(p1)
		b = self.dist(p2)
		cos_c = (a**2 + b**2 - p1.dist2(p2)) / 2 / a / b
		# imprecision in floats can lead to domain errors
		cos_c = min(max(cos_c, -1), 1)
		return acos(cos_c)
	
	def midpoint(self, other):
		return Point((self.x + other.x)/2, (self.y + other.y)/2)
	
	def __str__(self):
		return f"({self.x},{self.y})"
		
	def __eq__(self, other):
		if other is None:
			return False
		return self.x == other.x and self.y == other.y
	
	def __hash__(self):
		return hash(str(self))
	
	def left(self):
		return Point(self.x-1, self.y)
	
	def right(self):
		return Point(self.x+1, self.y)
	
	def up(self):
		return Point(self.x, self.y+1)
	
	def down(self):
		return Point(self.x, self.y-1)
	
	def inc(self, m):
		return Point(self.x + m[0], self.y + m[1])
	
	def coord(self):
		return (self.x, self.y)
		
	def coord_centered(self, shape):
		return (self.x + shape[0]//2, self.y + shape[1]//2)


def tri_area_from_coord(a, b, c):
	val = a.x*(b.y-c.y) + b.x*(c.y-a.y) + c.x*(a.y-b.y)
	return abs(val / 2)

def tri_area_from_dist(a, b, c):
	# Heron's Formula
	s = (a + b + c) / 2
	return sqrt(s * (s-a) * (s-b) * (s-c))


def clockwise(p):
	"""
	Returns the points in a clockwise order.
	
	p can be Point objects or complex numbers.
	"""
	
	p = sorted(p, key = str) # so it's always the same starting point
	center = sum(p)/4
	
	if isinstance(p[0], Point):
		compare = lambda a,b: 	(a.x - center.x) * \
								(b.y - center.y) - \
								(b.x - center.x) * \
								(a.y - center.y)
	else:
		compare = lambda a,b: 	(a.real - center.real) * \
								(b.imag - center.imag) - \
								(b.real - center.real) * \
								(a.imag - center.imag)
	
	p.sort(key = cmp_to_key(compare))
	return p