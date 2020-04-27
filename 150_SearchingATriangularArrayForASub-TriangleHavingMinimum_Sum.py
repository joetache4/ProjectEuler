"""
Problem 150 at ProjectEuler.net

In a triangular array of positive and negative integers, we wish to find a sub-triangle such that the sum of the numbers it contains is the smallest possible.

(https://projecteuler.net/project/images/p150.gif)

In the example below, it can be easily verified that the marked triangle satisfies this condition having a sum of −42.

We wish to make such a triangular array with one thousand rows, so we generate 500500 pseudo-random numbers s[k] in the range ±2e19, using a type of random number generator (known as a Linear Congruential Generator) as follows:

t := 0
for k = 1 up to k = 500500:
    t := (615949*t + 797807) modulo 2e20
    s[k] := t−2e19

Thus: s[1] = 273519, s[2] = −153582, s[3] = 450905 etc

Our triangular array is then formed using the pseudo-random numbers thus:
s1
s2  s3
s4  s5  s6 
s7  s8  s9  s10
...

Sub-triangles can start at any element of the array and extend down as far as we like (taking-in the two elements directly below it from the next row, the three elements directly below from the row after that, and so on).

The "sum of a sub-triangle" is defined as the sum of all the elements it contains.
Find the smallest possible sub-triangle sum.

ans: row: 7,  index: 7,  height: 886,  sum: -271248680

Note: This script finishes for me in 2 minutes.

Note 2: This algorithm is O(n^(3/2)). Naively computing the sum of sub-triangles is O(n^(5/2)).
"""

import sys
from math import sqrt

n = 1000  # triangle depth

# Program args: depth | "test"
do_test = False
try:
	do_test = sys.argv[1] == "test"
	n = int(sys.argv[1])
except:
	pass

# Implement the random number generator.
# Returns the triangle as a list.
def initial_triangle(depth):
	a = []
	size  = depth * (depth+1) // 2
	t19 = 2 << 18
	t20 = 2 << 19
	b = 0
	for k in range(1, size+1):
		b = (615949*b + 797807) % t20
		a.append(b - t19)
	return a

# Finds the minimum-sum sub-triangle.
# The main idea is that the sums for larger sub-triangles
# can be easily calculated from the sums of smaller sub-triangles.
def min_sub_triangle(triangle):
	# calculate depth from length
	depth = len(triangle)
	depth = int(sqrt(8 * depth + 1) - 1) // 2

	# current sums of sub-triangles	
	sum0 = [0 for x in range(len(triangle))]
	
	# lists that store previous sums
	sum1 = [0 for x in range(len(triangle))]
	sum2 = [0 for x in range(len(triangle))]

	# best solution so far
	min_sum = triangle[0]
	min_info = None

	# loop for each triangle height
	for d in range(1, depth+1):	
		# indexes to various parts of interest in the triangle
		self_index = 0
		child_index_1 = 1    # the first of two elements directly underneath
		child_index_2 = 2
		grandchild_index = 4 # the single element two rows below
		# loop for each triangle row
		for level in range(0, depth - d + 1):
			# loop for each triangle index
			for index in range(0, level + 1):
				# add parts together
				sum0[self_index] = triangle[self_index]
				try:
					sum0[self_index] += sum1[child_index_1] + sum1[child_index_2]
					sum0[self_index] -= sum2[grandchild_index]
				except:
					# ignore index out of bounds
					# happens at the bottom of the triangle when d=1,2
					pass
				# compare to minimum
				if sum0[self_index] < min_sum:
					min_sum = sum0[self_index]
					min_info = (level, index, d, min_sum)
				# going to next element in row, slide indices
				self_index += 1
				child_index_1 += 1
				child_index_2 += 1
				grandchild_index += 1
			# going to next row, indices go to next row
			child_index_1 += 1
			child_index_2 += 1
			grandchild_index += 2
		# going to next higher height, shift sums
		sum2 = sum1
		sum1 = sum0
		sum0 = sum2 # this will be overwritten next iteration
		
	return min_info


def test():
	print("Testing...")
	t = initial_triangle(1000)
	assert t[0] == 273519
	assert t[1] == -153582
	assert t[2] == 450905
	
	t = [15,-14,-7,20,-13,-5,-3,8,23,-26,1,-4,-5,-18,5,-16,31,2,9,28,3]
	assert min_sub_triangle(t) == (1, 1, 4, -42)
	print("[SUCCESS]")


if do_test:
	test()
else:
	triangle = initial_triangle(n)
	level, index, depth, min_sum = min_sub_triangle(triangle)
	print(f"row: {level},  index: {index},  height: {depth},  sum: {min_sum}")