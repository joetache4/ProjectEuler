"""
By replacing each of the letters in the word CARE with 1, 2, 9, and 6 respectively, we form a square number: 1296 = 36^2. What is remarkable is that, by using the same digital substitutions, the anagram, RACE, also forms a square number: 9216 = 96^2. We shall call CARE (and RACE) a square anagram word pair and specify further that leading zeroes are not permitted, neither may a different letter have the same digital value as another letter.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, find all the square anagram word pairs (a palindromic word is NOT considered to be an anagram of itself).

What is the largest square number formed by any member of such a pair?

NOTE: All anagrams formed must be contained in the given text file.


ans: 18769
"""

from math import sqrt, ceil, floor
from lib.num import bs_contains
from data.p098 import get_data

# can tell if two words are substitutions of each other
def sig(s):
	ind = {}
	ret = []
	for i in range(len(s)):
		c = s[i]
		try:
			ret.append(ind[c])
		except:
			ind[c] = i
			ret.append(i)
	return tuple(ret)

def permutation(a, b):
	if len(a) != len(b) or sorted(a) != sorted(b):
		return None
	perm = []
	for c in a:
		for i in range(len(b)):
			d = b[i]
			if c == d and i not in perm:
				perm.append(i)
				break
	return perm

def permute(i, p):
	i = str(i)
	ret = [0 for j in i]
	for j in range(len(i)):
		ret[p[j]] = i[j]
	return "".join(( str(d) for d in ret ))

words = get_data()
perms = {}
n     = -1


for i in range(len(words)-1):
	a = words[i]
	sig_a = sig(a)
	for j in range(i+1, len(words)):
		#if i == j:
		#	continue
		b = words[j]
		p = permutation(a,b)
		if p is not None:
			n = max(n, len(p))
			try: 
				perms[sig_a].append(p)
			except:
				perms[sig_a] = []
				perms[sig_a].append(p)

squares = [m*m for m in range(ceil(sqrt(10**(n))-1))]

ans = -1
for s in squares:
	sig_s = sig(str(s))
	for sig_w in perms:
		if sig_s == sig_w:
			for p in perms[sig_w]:
				i = permute(s, p)
				if i[0] == "0":
					continue
				i = int(i)
				if bs_contains(squares, i):
					ans = max(( ans, s, i ))
					
print(ans)