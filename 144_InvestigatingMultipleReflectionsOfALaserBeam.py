"""
In laser physics, a "white cell" is a mirror system that acts as a delay line for the laser beam. The beam enters the cell, bounces around on the mirrors, and eventually works its way back out.

The specific white cell we will be considering is an ellipse with the equation 4x2 + y2 = 100

The section corresponding to −0.01 ≤ x ≤ +0.01 at the top is missing, allowing the light to enter and exit through the hole.

The light beam in this problem starts at the point (0.0,10.1) just outside the white cell, and the beam first impacts the mirror at (1.4,-9.6).

Each time the laser beam hits the surface of the ellipse, it follows the usual law of reflection "angle of incidence equals angle of reflection." That is, both the incident and reflected beams make the same angle with the normal line at the point of incidence.

In the figure on the left, the red line shows the first two points of contact between the laser beam and the wall of the white cell; the blue line shows the line tangent to the ellipse at the point of incidence of the first bounce.

The slope m of the tangent line at any point (x,y) of the given ellipse is: m = −4x/y

The normal line is perpendicular to this tangent line at the point of incidence.

The animation on the right shows the first 10 reflections of the beam.

How many times does the beam hit the internal surface of the white cell before exiting?


ans: 354
"""


from math import sqrt

dot = lambda a,b: a[0]*b[0] + a[1]*b[1]

# see https://en.wikipedia.org/wiki/Cross_product
def sin_ang(a,b):
	s = dot(a,a)*dot(b,b) # s = 1 if a,b normalized
	return sqrt(1 - (dot(a,b)**2)/s)

def cos_ang(a,b):
	return dot(a,b) / sqrt(dot(a,a)*dot(b,b))

def reflect(a,b):
	perp = (-4*b[0], -b[1])
	in_ray = (a[0]-b[0], a[1]-b[1])
	c = cos_ang(in_ray, perp)
	s = sin_ang(in_ray, perp)
	out_ray = (c*perp[0] - s*perp[1], s*perp[0] + c*perp[1])
	return out_ray # not normalized

def next(p1,p2):
	x = p2[0]
	y = p2[1]
	m = reflect(p1,p2)
	m = m[1]/m[0]
	
	a = 4 + m*m
	b = 2*m*y - 2*m*m*x
	c = m*m*x*x - 2*m*y*x + y*y - 100
	
	x_1 = (-b + sqrt(b*b - 4*a*c))/2/a
	x_2 = (-b - sqrt(b*b - 4*a*c))/2/a
	y_1 = m*x_1 - m*x + y
	y_2 = m*x_2 - m*x + y
	
	# choose the one that's further from p2
	d1 = (x - x_1)**2 + (y - y_1)**2
	d2 = (x - x_2)**2 + (y - y_2)**2
	if d1 > d2:
		return (x_1, y_1)
	else:
		return (x_2, y_2)

a = (0,10.1)
b = (1.4, -9.6)
count = 0
while not (abs(b[0]) <= 0.01 and b[1] > 0):
	a, b = b, next(a, b)
	count += 1
print(count)