'''
Bozo sort, not to be confused with the slightly less efficient bogo sort, consists out of checking if the input sequence is sorted and if not swapping randomly two elements. This is repeated until eventually the sequence is sorted.

If we consider all permutations of the first 4 natural numbers as input the expectation value of the number of swaps, averaged over all 4! input sequences is 24.75.
The already sorted sequence takes 0 steps.

In this problem we consider the following variant on bozo sort.
If the sequence is not in order we pick three elements at random and shuffle these three elements randomly.
All 3!=6 permutations of those three elements are equally likely.
The already sorted sequence will take 0 steps.
If we consider all permutations of the first 4 natural numbers as input the expectation value of the number of shuffles, averaged over all 4! input sequences is 27.5.

Consider as input sequences the permutations of the first 11 natural numbers.
Averaged over all 11! input sequences, what is the expected number of shuffles this sorting algorithm will perform?

Give your answer rounded to the nearest integer.

ans: 48271207
'''

"""
Solution method:

Scramble: a description of a permutation given by the number of swaps (2-shifts) and larger n-shifts

Each permutation has one scramble.
Each scramble has multiple permutations.
Permutations of the same scramble have the same transition-scramble distribution.

1. 	Create a representative permutation for each scramble

2. 	Calculate transition distribution.

3. 	Solve expected # of swaps system of equations

	S(0) = 0
	S(2) = 1 + P(S(2) -> S(2))*S(2) + P(S(2) -> S(2,2))*S(2,2) + ... + P(S(2) -> S(11))*S(11)
	...

	where S(i) is the expected number of swaps to go from scramble i to scramble 0 (the "no-scramble")

4. 	Average results: ans = sum(count_perms(scramble n)*S(n)) / 11!
"""

import math
from collections import Counter
import numpy as np

n = 11

# 3-swap, type says how to swap them
def swap(arr, i, j, k, type):
	if type == 0:
		# left shift
		arr[i], arr[j], arr[k] = arr[j], arr[k], arr[i]
	elif type == 1:
		# right shift
		arr[i], arr[j], arr[k] = arr[k], arr[i], arr[j]
	elif type == 2:
		# 1-2 swap
		arr[i], arr[j] = arr[j], arr[i]
	elif type == 3:
		# 2-3 swap
		arr[j], arr[k] = arr[k], arr[j]
	elif type == 4:
		# 1-3 swap
		arr[i], arr[k] = arr[k], arr[i]
	elif type == 5:
		# nothing
		pass
	return arr

# create every possible scramble for an array of given length
def scrambles(length, s = None, begin = None):
	if s is None:
		s = [[0]]
	if begin is None:
		begin = []
	for swap in range(2, length+1):
		if len(begin) > 0 and swap < begin[-1]:
			continue
		if sum(begin) + swap > length:
			break
		new_begin = begin.copy()
		new_begin.append(swap)
		s.append(new_begin)
		scrambles(length, s, new_begin)
	return s

# create an arbitrary array of the given length with the given scramble
# e.g. scrambles = [2,2,3] means two swaps and one 3-shift
def representative_scramble(length, scramble):
	if sum(scramble) > length:
		raise ValueError
		
	arr = [i for i in range(length)]
	
	# every n-cycle can be made by n-1 consecutive swaps
	i = 0
	for s in scramble:
		for j in range(0, s-1):
			arr[i+j], arr[i+j+1] = arr[i+j+1], arr[i+j]
		i += s
	
	return arr

# combinatorial choose
def C(n, r):
	f = math.factorial
	return f(n) // f(r) // f(n-r)

# return the number of permutations with the given scramble
def count_perms(length, scramble):
	total = 1
	if scramble == [0]:
		return 1
	for s in scramble:
		#print(f"+{num}")		
		total *= C(length, s) * math.factorial(s-1) # choose s items, shift them
		length -= s # chosen s items cannot be chosen again
	# divide by repeated swaps
	# e.g. a [2,2] scramble double counts; a [2,2,2] 6x-counts
	for swap,count in Counter(scramble).items():
		total //= math.factorial(count)
	return total

# find out how the arr is scrambled
def scramble(arr):
	scramble = []
	for i in range(len(arr)):
		if arr[i] in [-1, i]:
			continue
		s = 0
		while arr[i] != -1:
			arr[i], i = -1, arr[i]
			s += 1
		scramble.append(s)
	scramble.sort()
	if scramble == []:
		return [0]
	return scramble

# concat array into string for use as a key to a dict
def key(arr):
	return "-".join((str(a) for a in arr))

# count the ways a scrambled array can transition into another scramble
# divide by total to get a probability
def trans_dist(arr):
	num_scrambles = {key(scramble):0 for scramble in scrambles(len(arr))}
	
	for i in range(len(arr)-2):
		for j in range(i+1, len(arr)-1):
			for k in range(j+1, len(arr)):
				for type in range(6):
					swapped = swap(arr.copy(), i, j, k, type)
					s = key(scramble(swapped))
					num_scrambles[s] += 1
	
	# convert to list of probabilities
	total = sum((v for k,v in num_scrambles.items()))
	#num_scrambles = {k: v / total for k,v in num_scrambles.items()}
	num_scrambles = [num_scrambles[key(s)] / total for s in scrambles(len(arr))]
	
	return num_scrambles

# compile transition distributions into a matrix
def transition_matrix(length):
	s = scrambles(length)
	
	mat = np.zeros((len(s), len(s)))
	
	for i, scramble in zip(range(len(s)), s):
		p = representative_scramble(length, scramble)
		dist = trans_dist(p)
		for j, prob in zip(range(len(s)), dist):
			mat[i, j] = prob
	
	# the first row is special in that the transition from a 
	# totally correct sequence to any other needs to be 0
	# including [0] -> [0] (otherwise this leads to non-unique solutions)
	for i in range(len(s)):
		mat[0, i] = 0
	
	return mat

def expected_swap_count(length):
	# solve expected swap count system
	A = transition_matrix(length)
	A = A - np.eye(A.shape[0])
	b = -1 * np.ones((A.shape[0], 1))
	b[0,0] = 0
	expected_by_scramble = np.linalg.inv(A).dot(b)
	
	# weighted average
	average = 0
	s = scrambles(length)
	for i, scramble in zip(range(len(s)), s):
		average += count_perms(length, scramble) * expected_by_scramble[i, 0]
	average /= math.factorial(length)
	
	return average	
	
def test():
	# Note that same scramble = same transition dist	
	assert trans_dist([0,1,2,4,3]) == trans_dist([2,1,0,3,4]) # one swap
	assert trans_dist([0,1,2,3,5,6,4,7,8,9,11,10]) == trans_dist([6,1,2,11,4,5,9,7,8,0,10,3]) # one swap and one 3-shift

	count = sum((count_perms(n, scramble) for scramble in scrambles(n)))
	assert count == math.factorial(n)

	s = [4,7]
	assert scramble(representative_scramble(n, s)) == s

	assert math.isclose(expected_swap_count(4), 27.5)
	assert math.isclose(expected_swap_count(11), 48271206.73668042)

test()

ans = expected_swap_count(n)
print(f"exact = {ans}")
print(f"ans   = {int(ans + 0.5)}")