"""
A common security method used for online banking is to ask the user for three random characters from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.

The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible secret passcode of unknown length.

ans: 73162890
"""

from _data.p079 import get_data

codes = set(get_data())
codes = [str(code) for code in codes]

present = set()
for code in codes:
	for num in str(code):
		present.add(num)
present = list(present)
present.sort()

next = {p: set() for p in present}

for code in codes:
	code = str(code)
	next[code[0]].add(code[1])
	next[code[0]].add(code[2])
	next[code[1]].add(code[2])

next = {p: list(next[p]) for p in next}

#print(present)
#print(next)

def seq(test_arr, a, b):
	try:
		ind_a = test_arr.index(a)
		ind_b = test_arr[::-1].index(b)
		return ind_a < (len(test_arr) - ind_b - 1)
	except ValueError:
		# not in list
		return False

assert seq([1,2], 1, 2)
assert not seq ([2,1], 1, 2)

def count_not_met(test_arr, present, next):
	count = 0
	for p in present:
		if not p in test_arr:
			count += 1
	for k,v in next.items():
		for n in v:
			if not seq(test_arr, k, n):
				count += 1
	return count

def find_min_length(present, next, test = None, min_len = 999):
	if test is None:
		test = []
	
	if len(test) >= min_len:
		if len(test) == 8: # yeah, this sucks
			print("".join(test))
		return min_len
	
	not_met = count_not_met(test, present, next)
	if not_met == 0:
		if len(test) == 8:
			print(test)
		return len(test)
	
	for p in present:
		test.append(p)
		new_not_met = count_not_met(test, present, next)
		if new_not_met < not_met:
			min_len = min(min_len, find_min_length(present, next, test, min_len))
		test.pop()
	
	return min_len

print(find_min_length(present, next))
