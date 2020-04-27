"""
A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3, and a fly, F, sits in the opposite corner. By travelling on the surfaces of the room the shortest "straight line" distance from S to F is 10 and the path is shown on the diagram.

However, there are up to three "shortest" path candidates for any given cuboid and the shortest route doesn't always have integer length.

It can be shown that there are exactly 2060 distinct cuboids, ignoring rotations, with integer dimensions, up to a maximum size of M by M by M, for which the shortest route has integer length when M = 100. This is the least value of M for which the number of solutions first exceeds two thousand; the number of solutions when M = 99 is 1975.

Find the least value of M such that the number of solutions first exceeds one million.


ans: 1818
"""


'''
Solution Method:

Let X,Y,Z be the side lengths of the cuboid. 
Let L be the shortest length from one corner to its opposite.

Assuming X >= Y >= Z, then L = sqrt( X**2 + (Y+Z)**2 ),
which can be visualized when unfolding the cuboid along the X edge.

So, find Pythagorean Triples a,b,c and count the ways a=X and b=Y+Z.
'''


from math import sqrt

target = 10**6

cuboids = set()
a = 3
while True:
	for b in range(2, 2*a+1):
		c = sqrt(a**2 + b**2)
		if c == int(c):
			x = a
			# "fold" the pythagorean triangle at side b so that the 2 new sides are <= side a
			for fold_index in range(max(1, b-a), min(b, a+1)):
				y = fold_index
				z = b - fold_index
				cuboids.add(( *sorted(( x,y,z )) ))
	if len(cuboids) > target:
		break
	a += 1

print(a)
print(len(cuboids))