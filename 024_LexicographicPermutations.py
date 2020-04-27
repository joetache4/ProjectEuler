"""

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

ans: 2783915460
"""

# more efficient to convert 10^6 to factorial numbering system but I'm too lazy for that

import sys

all = [x for x in range(10)]

count = 1

for a in all:
	for b in all:
		if b == a: continue
		for c in all:
			if c in [a,b]: continue
			for d in all:
				if d in [a,b,c]: continue
				for e in all:
					if e in [a,b,c,d]: continue
					for f in all:
						if f in [a,b,c,d,e]: continue
						for g in all:
							if g in [a,b,c,d,e,f]: continue
							for h in all:
								if h in [a,b,c,d,e,f,g]: continue
								for i in all:
									if i in [a,b,c,d,e,f,g,h]: continue
									for j in all:
										if j in [a,b,c,d,e,f,g,h,i]: continue
										if count == 10**6:
											ans = [str(x) for x in [a,b,c,d,e,f,g,h,i,j]]
											print("".join(ans))
											sys.exit()
										count += 1