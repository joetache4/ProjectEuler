"""
The nth term of the sequence of triangle numbers is given by, tn = ½n(n+1); so the first ten triangle numbers are:

1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...

By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t10. If the word value is a triangle number then we shall call the word a triangle word.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?

ans: 162
"""

from _data.p042 import get_data

words = get_data()
longest = max(len(s) for s in words)

def get_triangle_nums(max):
	t, n = 1, 2
	while t < max:
		yield t
		t += n
		n += 1

def value(s):
	s = s.lower()
	return sum((ord(c)-96 for c in s))

assert value("SKY") == 55
	
tri_nums  = list(get_triangle_nums(value("Z" * longest)))
tri_words = []

for s in words:
	if value(s) in tri_nums:
		tri_words.append(s)

print(tri_words)
print(f"ans = {len(tri_words)}")