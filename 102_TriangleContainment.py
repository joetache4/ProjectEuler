"""
Three distinct points are plotted at random on a Cartesian plane, for which -1000 ≤ x, y ≤ 1000, such that a triangle is formed.

Consider the following two triangles:

A(-340,495), B(-153,-910), C(835,-947)

X(-175,41), Y(-421,-714), Z(574,-645)

It can be verified that triangle ABC contains the origin, whereas triangle XYZ does not.

Using triangles.txt (right click and 'Save Link/Target As...'), a 27K text file containing the co-ordinates of one thousand "random" triangles, find the number of triangles for which the interior contains the origin.

NOTE: The first two examples in the file represent the triangles in the example given above.


ans: 228
"""

from _data.p102 import get_data

triangles = get_data()
o = (0,0)

def area(a, b, c): 
	val = a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1])
	return abs(val / 2)

def contains_origin(tri):
	a = (tri[0], tri[1])
	b = (tri[2], tri[3])
	c = (tri[4], tri[5])
	return area(a,b,c) == area(o,b,c) + area(a,o,c) + area(a,b,o)

print(sum(( 1 for tri in triangles if contains_origin(tri) )))