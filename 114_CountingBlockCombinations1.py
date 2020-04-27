"""
A row measuring seven units in length has red blocks with a minimum length of three units placed on it, such that any two red blocks (which are allowed to be different lengths) are separated by at least one grey square. There are exactly seventeen ways of doing this.
p114.png

How many ways can a row measuring fifty units in length be filled?

NOTE: Although the example above does not lend itself to the possibility, in general it is permitted to mix block sizes. For example, on a row measuring eight units in length you could use red (3), grey (1), and red (4).

ans: 16475640049
"""

def num_fill(length):
	mem = {}
	return num_fill_r(True, length, mem) + num_fill_r(False, length, mem)

def num_fill_r(red, length, mem):
	if red:
		if length == 3:
			return 1
		elif length < 3:
			return 0
	else:
		if length == 1:
			return 1
		elif length < 1:
			return 0
	
	if (red, length) in mem:
		return mem[(red, length)]
	
	count = 1
	if red:
		for i in range(3, length+1):
			count += num_fill_r(False, length-i, mem)
	else:
		for i in range(1, length+1):
			count += num_fill_r(True, length-i, mem)
	
	mem[(red,length)] = count
	return count

assert num_fill(7) == 17
print(num_fill(50))