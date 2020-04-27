"""
A row of five grey square tiles is to have a number of its tiles replaced with coloured oblong tiles chosen from red (length two), green (length three), or blue (length four).

If red tiles are chosen there are exactly seven ways this can be done.
png116_1.png

If green tiles are chosen there are three ways.
png116_2.png

And if blue tiles are chosen there are two ways.
png116_3.png

Assuming that colours cannot be mixed there are 7 + 3 + 2 = 12 ways of replacing the grey tiles in a row measuring five units in length.

How many different ways can the grey tiles in a row measuring fifty units in length be replaced if colours cannot be mixed and at least one coloured tile must be used?

NOTE: This is related to Problem 117.

ans: 20492570929
"""

def count(grey_len, color_len, cache = {}, empty = True):
	try:
		return cache[(grey_len, color_len, empty)]
	except KeyError:
		pass
	
	a = 0
	if grey_len < 0:
		a = 0
	elif grey_len < color_len:
		if empty:
			a = 0
		else:
			a = 1
	#elif grey_len <= 0: 
	#	a = 0
	elif grey_len == color_len:
		if empty:
			a = 1
		else:
			a = 2
	elif grey_len > color_len:
		for i in range(color_len):
			a += count(grey_len - i - color_len, color_len, cache, False)
		a += count(grey_len - color_len, color_len, cache, empty)
	
	cache[(grey_len, color_len, empty)] = a
	return a

w = 5
print(count(w,2) + count(w,3) + count(w,4))
w = 50
print(count(w,2) + count(w,3) + count(w,4))