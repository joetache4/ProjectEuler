"""
Looking at the table below, it is easy to verify that the maximum possible sum of adjacent numbers in any direction (horizontal, vertical, diagonal or anti-diagonal) is 16 (= 8 + 7 + 1).
−2	5	3	2
9	−6	5	1
3	2	7	3
−1	8	−4	  8

Now, let us repeat the search, but on a much larger scale:

First, generate four million pseudo-random numbers using a specific form of what is known as a "Lagged Fibonacci Generator":

For 1 ≤ k ≤ 55, sk = [100003 − 200003k + 300007k^3] (modulo 1000000) − 500000.
For 56 ≤ k ≤ 4000000, s_k = [s_k−24 + s_k−55 + 1000000] (modulo 1000000) − 500000.

Thus, s_10 = −393027 and s_100 = 86613.

The terms of s are then arranged in a 2000×2000 table, using the first 2000 numbers to fill the first row (sequentially), the next 2000 numbers to fill the second row, and so on.

Finally, find the greatest sum of (any number of) adjacent entries in any direction (horizontal, vertical, diagonal or anti-diagonal).

ans: 52852124
"""

import numpy as np

def rand():
	s = []
	for k in range(1, 56):
		sk = (100003 - 200003*k + 300007*k**3) % 1000000 - 500000
		yield sk
		s.append(sk)
	for k in range(56, 4000001):
		sk = (s[55-24] + s[0] + 1000000) % 1000000 - 500000
		yield sk
		s.append(sk)
		s.pop(0)

def test_rand():
	a = [x for x in rand()]
	assert a[ 10-1] == -393027
	assert a[100-1] ==   86613

# skews an np.array by appending zeros on the sides
def skew(values):
	new_arr = []
	for i in range(len(values)):
		skewed = [0]*i + values[i].tolist() + [0]*(len(values)-i-1) # append using list +
		new_arr.append(skewed)
	return np.array(new_arr)

def max_sum():
	print("Creating pseudorandom array")
	values = np.array([x for x in rand()]).reshape((2000, 2000))
	print("Finding max vertical sum")
	max_val = max_vertical_sum(values)
	print("Finding max horizontal sum")
	max_val = max(max_val, max_vertical_sum(values.transpose()))
	print("Finding max diagonal (/) sum")
	max_val = max(max_val, max_vertical_sum(skew(values)))
	print("Finding max diagonal (\) sum")
	max_val = max(max_val, max_vertical_sum(skew(values[::-1])))
	print(f"max: {max_val}")

# finds the greatest sum of consecutive values in each column of a 2 dimensional np.array
def max_vertical_sum(values):
	top, mid, bot, tot = max_vertical_sum_helper(values)
	return max(mid)

# helps find the greatest sum of consecutive values in each column of a 2 dimensional np.array
# recursive binary splitting of rows in values
# i.e., {2000 rows} -> {1000, 1000 rows} -> {500,500,500,500 rows} -> ...
# method returns what I call top, middle, bottom, total sums
# top: greatest sum of a sequence that contains the topmost value in the chunk
# mid: greatest sum of a any sequence in the chunk
# bot: greatest sum of a sequence that contains the bottommost value in the chunk
# tot: the sum of all elements in the chunk
# the parent chunk can then easily calculate its own top, mid, bottom, and total
# sums from the sums of its two child chunks
def max_vertical_sum_helper(values):
	if len(values) == 0:
		return (None, None, None, None)
	if len(values) == 1:
		return (values[0], values[0], values[0], values[0])
		
	a_top, a_mid, a_bot, a_tot = max_vertical_sum_helper(values[:len(values)//2 ]) # a is "on top"
	b_top, b_mid, b_bot, b_tot = max_vertical_sum_helper(values[ len(values)//2:])
	if a_top is None:
		return (b_top, b_mid, b_bot, b_tot)
	if b_top is None:
		return (a_top, a_mid, a_bot, a_tot)

	new_top = np.maximum(a_top,	a_tot + b_top)
	new_mid = np.maximum(a_mid, np.maximum(b_mid, a_bot + b_top))
	new_bot = np.maximum(b_bot,	b_tot + a_bot)
	new_tot = a_tot + b_tot
	
	return (new_top, new_mid, new_bot, new_tot)

max_sum()