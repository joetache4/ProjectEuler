"""
If a box contains twenty-one colored discs, composed of fifteen blue discs and six red discs, and two discs were taken at random, it can be seen that the probability of taking two blue discs, P(BB) = (15/21)×(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two blue discs at random, is a box containing eighty-five blue discs and thirty-five red discs.

By finding the first arrangement to contain over 10^12 = 1,000,000,000,000 discs in total, determine the number of blue discs that the box would contain.

ans: 756872327473
"""

# see http://fs.unm.edu/SolvingDiophantineEquations.pdf

from math import sqrt

# From hypergeometric distribution, we see 2*choose(B, 2) = choose(N, 2).
# This reduces to solving the quadratic N^2 - N - 2B(B-1).
# An integer N solution exists when sqrt(1 + 8B(B-1)) is an integer.
# Or, in other words, s^2 = 1 + 8B(B-1) for some integer s.
# But this is another quadratic, 
# and it has a solution when t^2 = 32s^2 + 32 for some integer t.
# This means we need to solve the new Diophantine equation, 32s^2 - t^2 + 32 = 0.

# See page 115 of Cira & Smarandache (2014) http://fs.unm.edu/SolvingDiophantineEquations.pdf

# All solutions to this Diophantine equation are found by
# multiplying a basis matrix (raised to a power) and the minimal solutions.
# The smallest solutions with positive x_0 are (1,8) and (1,-8).
# Find basis matrix:

s = 32
t = 1
for i in range(2,10**6):
	q = sqrt(t/s*(i-1)*(i+1))
	if q == int(q) and s*q/t == int(s*q/t):
		print((i, q))
		print((s*q/t, i))
		break
		
# The basis matrix is A = [17, 3; 96, 17].
# The eigenvalues are 17 +- 12*sqrt(2).
# The eigenvectors are [sqrt(2)/8; 1] and [-sqrt(2)/8; 1].
# The solutions are +-(A^n * [1, 8]) and +-(A^n * [1, -8]),
# but since the results are ultimately squared, the sign is unimportant.

target = 10**12

# A is a 2x2 matrix.
# B is a 2-vector or a 2x2 matrix.
# Each are listed by column.
def mat_mult(A, B):
	res = [A[0]*B[0] + A[2]*B[1], A[1]*B[0] + A[3]*B[1]]
	if len(B) > 2: # this isn't used anymore
		res.append(A[0]*B[2] + A[2]*B[3])
		res.append(A[1]*B[2] + A[3]*B[3])
	return res

# Number of blue discs.
def B(s):
	return (8 + int(sqrt(32*s*s + 32))) // 16

# Total number of discs.
def N(b):
	return (1 + int(sqrt(1 + 8*b*(b-1)))) // 2

def main():
	A = [17, 96, 3, 17]
	b0 = [1, 8]
	b1 = [1, -8]

	assert mat_mult(A, b0) == [41, 232]
	assert mat_mult(A, b1) == [-7, -40]
	assert mat_mult(A, A) == [577, 3264, 102, 577]
	
	while True:
		sols = [B(s) for s in [b0[0], b1[0]]]
		sols.sort()
		print(sols)
		for b in sols:
			n = N(b)
			assert n*(n-1) == 2*b*(b-1)
			if n > target:
				print(b)
				return
		b0 = mat_mult(A, b0)
		b1 = mat_mult(A, b1)

main()