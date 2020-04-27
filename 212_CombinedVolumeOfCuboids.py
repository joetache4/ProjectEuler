"""
An axis-aligned cuboid, specified by parameters { (x0,y0,z0), (dx,dy,dz) }, consists of all points (X,Y,Z) such that x0 ≤ X ≤ x0+dx, y0 ≤ Y ≤ y0+dy and z0 ≤ Z ≤ z0+dz. The volume of the cuboid is the product, dx × dy × dz. The combined volume of a collection of cuboids is the volume of their union and will be less than the sum of the individual volumes if any cuboids overlap.

Let C1,...,C50000 be a collection of 50000 axis-aligned cuboids such that Cn has parameters

x0 = S6n-5 modulo 10000
y0 = S6n-4 modulo 10000
z0 = S6n-3 modulo 10000
dx = 1 + (S6n-2 modulo 399)
dy = 1 + (S6n-1 modulo 399)
dz = 1 + (S6n modulo 399)

where S1,...,S300000 come from the "Lagged Fibonacci Generator":

For 1 ≤ k ≤ 55, Sk = [100003 - 200003k + 300007k3]   (modulo 1000000)
For 56 ≤ k, Sk = [Sk-24 + Sk-55]   (modulo 1000000)

Thus, C1 has parameters {(7,53,183),(94,369,56)}, C2 has parameters {(2383,3563,5079),(42,212,344)}, and so on.

The combined volume of the first 100 cuboids, C1,...,C100, is 723581599.

What is the combined volume of all 50000 cuboids, C1,...,C50000 ?

ans: 328968937309
"""

# http://tmc.web.engr.illinois.edu/easyklee4_13.pdf

import math
from collections import deque
from statistics import median
from random import randint

import random

class LaggedFibonacciGenerator:
	def __init__(self):
		self.seq = []
	def get(self):
		k, v = len(self.seq)+1, 0
		if k <= 55:
			v = 100003 - 200003*k + 300007*k**3
		else:
			v = self.seq[k-25] + self.seq[k-56]
		v = v % 1000000
		self.seq.append(v)
		return v

class Cuboid():

	@staticmethod
	def generate(rng, dim = 3, maxoffset = 9999, maxwidth = 399):
		maxoffset += 1
		coord = []
		for i in range(dim):
			coord.append(rng.get() % maxoffset)
		for i in range(dim):
			coord.append(coord[i] + 1 + (rng.get() % maxwidth))
		return Cuboid(*coord)
	
	@staticmethod
	def domain(C):
		D = C[0].copy()
		for cub in C:
			for axis in range(D.dim):
				D.set(axis, 0, min(D.get(axis, 0), cub.get(axis, 0)))
				D.set(axis, 1, max(D.get(axis, 1), cub.get(axis, 1)))
		return D
	
	def __init__(self, *coord):
		self.coord = list(coord)
		self.dim   = len(self.coord)//2
	
	def copy(self):
		return Cuboid(*self.coord)
	
	def get(self, axis, endpoint):
		return self.coord[self.dim * endpoint + axis]
		
	def set(self, axis, endpoint, newval):
		self.coord[self.dim * endpoint + axis] = newval
	
	def volume(self):
		return math.prod(( self.get(i,1) - self.get(i,0) for i in range(self.dim) ))
	
	def intersect(self, other):
		for i in range(self.dim):
			if self.get(i, 1) <= other.get(i, 0) or self.get(i, 0) >= other.get(i, 1):
				return None
		cub = self.copy()
		for i in range(self.dim):
			cub.set(i, 0, max(self.get(i, 0), other.get(i, 0)))
			cub.set(i, 1, min(self.get(i, 1), other.get(i, 1)))
		return cub
	
	# returns an interval or None for each axis indicating presence of "slabs"
	def slab(self, D):
		result = [None for i in range(self.dim)]
		lo	   = [self.get(i, 0) <= D.get(i, 0) for i in range(self.dim)]
		hi	   = [self.get(i, 1) >= D.get(i, 1) for i in range(self.dim)]
		for i in range(self.dim):
			if all((lo[j] and hi[j] for j in range(self.dim) if j != i)):
				result[i] = (max(D.get(i, 0), self.get(i, 0)), min(D.get(i, 1), self.get(i, 1)))
		return result
	
	# readjust sides inside slabs to length zero, volume may reduce to 0
	def simplify(self, slabs):
		for axis in range(self.dim):
			new_x0 = self.get(axis, 0)
			new_x1 = self.get(axis, 1)
			for interval in slabs[axis]:
				if interval[0] <= self.get(axis, 0):
					new_x0 -= (min(self.get(axis, 0), interval[1]) - interval[0])
				if interval[0] <= self.get(axis, 1):
					new_x1 -= (min(self.get(axis, 1), interval[1]) - interval[0])
			self.set(axis, 0, new_x0)
			self.set(axis, 1, new_x1)
	
	# cut cuboid into 2 parts, at most one part can be None
	def cut(self, axis, val):
		if val <= self.get(axis, 0):
			return (None, self)
		elif val >= self.get(axis, 1):
			return (self, None)
		else:
			result = (self.copy(), self.copy())
			result[0].set(axis, 1, val)
			result[1].set(axis, 0, val)
			return result

# merge a list of intervals, (start, stop), by combining those that overlap
def merge_intervals(intervals):
	if len(intervals) == 0:
		return []
	intervals.sort()
	result = []
	(start_candidate, stop_candidate) = intervals[0]
	for (start, stop) in intervals[1:]:
		if start <= stop_candidate:
			stop_candidate = max(stop, stop_candidate)
		else:
			result.append((start_candidate, stop_candidate))
			start_candidate, stop_candidate = start, stop
	result.append((start_candidate, stop_candidate))
	return result

# volume of all cuboids combined
def combined_volume(C):
	D = Cuboid.domain(C)
	return D.volume() - measure(C, D)

# find volume of empty space inside Domain
def measure(C, D, cutaxis = 0):
	if len(C) < 3:
		return measure_direct(C, D)
	else:
		C, D = simplify(C, D)
		if len(C) == 0:
			return D.volume()
		CL, DL, CR, DR = cut(C, D, cutaxis)
		m = 0
		if DL:
			m += measure(CL, DL, (cutaxis+1)%D.dim)
		if DR:
			m += measure(CR, DR, (cutaxis+1)%D.dim)
		return m

# naive measure by adding/subtracting intersections
def measure_direct(C, D):
	m = D.volume()
	if len(C) == 0:
		return m
	elif len(C) == 1:
		try:
			m -= C[0].volume()
		except:
			pass
		return m
	elif len(C) == 2:
		try:
			m -= C[0].volume()
		except:
			pass
		try:
			m -= C[1].volume()
		except:
			pass
		try:
			m += C[0].intersect(C[1]).volume()
		except:
			pass
		return m

# reduce size of C and D while retaining volume of empty space
def simplify(C, D):
	new_C = []
	# get all slabs
	slabs = [[] for i in range(D.dim)]
	for cub in C:
		slab = cub.slab(D)
		for i in range(D.dim):
			if not slab[i]: continue
			slabs[i].append(slab[i])
	# combine slabs into a non-overlapping list of intervals
	for i in range(D.dim):
		slabs[i] = merge_intervals(slabs[i])
	#simplify D
	D.simplify(slabs)
	# simplify each cuboid, keep only if positive volume
	for cub in C:
		cub.simplify(slabs)
		if cub.volume() > 0:
			new_C.append(cub)
	return new_C, D

# cut C and D into 2 parts 
def cut(C, D, cutaxis):
	# find median of random sample
	sample = min(63, 2*len(C)+1)
	edges = [C[randint(0, len(C)-1)].get(cutaxis, randint(0, 1)) for i in range(sample)]
	edges.sort()
	m = median(edges)
	# cut, some cuboids are only on one side of the cut
	DL, DR = D.cut(cutaxis, m)
	CL, CR = [], []
	for cub in C:
		l, r = cub.cut(cutaxis, m)
		if l:
			CL.append(l)
		if r:
			CR.append(r)
	return CL, DL, CR, DR


rng = LaggedFibonacciGenerator()
C = [Cuboid.generate(rng) for i in range(100)]
assert combined_volume(C) == 723581599

rng = LaggedFibonacciGenerator()
C = [Cuboid.generate(rng) for i in range(50000)]
ans = combined_volume(C)
print(ans)
assert ans == 328968937309