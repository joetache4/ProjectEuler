"""
It is easily proved that no equilateral triangle exists with integral length sides and integral area. However, the almost equilateral triangle 5-5-6 has an area of 12 square units.

We shall define an almost equilateral triangle to be a triangle for which two sides are equal and the third differs by no more than one unit.

Find the sum of the perimeters of all almost equilateral triangles with integral side lengths and area and whose perimeters do not exceed one billion (1,000,000,000).


ans: 518408346
"""

from math import isqrt

def heronian_perimeter(a,b,c):
	p = a + b + c
	ar2 = p * (-a+b+c) * (a-b+c) * (a+b-c)
	ar = isqrt(ar2)
	if ar2 == ar**2 and ar % 4 == 0:
		return p
	return 0

ans = 0
for x in range(3, (10**9)//3 + 1, 2): # 1,1,2 is not Heronian, so skip it for simplicity's sake
	ans += heronian_perimeter2(x, x, x+1)
	ans += heronian_perimeter2(x, x, x-1)
print(ans)