"""
The points P (x1, y1) and Q (x2, y2) are plotted at integer co-ordinates and are joined to the origin, O(0,0), to form ΔOPQ.

There are exactly fourteen triangles containing a right angle that can be formed when each co-ordinate lies between 0 and 2 inclusive; that is,
0 ≤ x1, y1, x2, y2 ≤ 2.

Given that 0 ≤ x1, y1, x2, y2 ≤ 50, how many right triangles can be formed?

ans: 14234
"""

n = 50

points = []

index = 0
for x in range(n + 1):
	for y in range(n + 1):
		points.append((x, y))
points.pop(0)

count = 0

for i in range(len(points) - 1):
	for j in range(i + 1, len(points)):
		p1 = points[i]
		p2 = points[j]
		
		a = p1[0]**2 + p1[1]**2
		b = p2[0]**2 + p2[1]**2
		c = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
		a, b, c = sorted((a, b, c))
		if c == a + b:
			count += 1

print(count)