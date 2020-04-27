"""
We can easily verify that none of the entries in the first seven rows of Pascal's triangle are divisible by 7:
  	  	  	  	  	  	 1
  	  	  	  	  	 1 	  	 1
  	  	  	  	 1 	  	 2 	  	 1
  	  	  	 1 	  	 3 	  	 3 	  	 1
  	  	 1 	  	 4 	  	 6 	  	 4 	  	 1
  	 1 	  	 5 	  	10 	  	10 	  	 5 	  	 1
1 	  	 6 	  	15 	  	20 	  	15 	  	 6 	  	 1

However, if we check the first one hundred rows, we will find that only 2361 of the 5050 entries are not divisible by 7.

Find the number of entries which are not divisible by 7 in the first one billion (109) rows of Pascal's triangle.


ans: 2129970655314432
"""


# https://www2.edc.org/makingmath/mathprojects/pascal/pascal.patterns.pdf
# C(n,k) is divisible by prime p iff adding k and n-k has no "carries" in base p
# Let n = ab...z in base 7. There are prod((1+a)(1+b)...(1+z)) pairs (n, n-k)
# of non-negative integers that add to n w/o carries - and so not divisible by p.

# Solution method:
# Define [ab...z] to be the total number of p-free numbers up to and including row n
# (Remember that Pascal's Triangle in 0-indexed)
# Then:
#      [z] = sum(1 to z) inclusive
# [ab...z] = [(a-1)(p-1)...(p-1)] + a*p*...*p + (a+1)*[b...z]
# (Leading zeros are truncated)


##########

from lib.num import base

def cumsum(s, p, mem = {}):
	s = str(int(s)) # remove leading 0s
	try:
		return mem[s]
	except KeyError:
		n = int(s)
		if n in range(p+1):
			return (n+1) * (n) // 2
		else:
			d = int(s[0])
			l = len(s) - 1
			r = str(d-1) + (str(p-1)*l)
			t = s[1:]
			#print(f"cumsum({s}) = cumsum({r}) + {f} * cumsum({t})")
			ans = cumsum(r,p) + d*(p**l) + (d+1)*cumsum(t,p)
			mem[s] = ans
			return ans

def main(n, p = 7):
	if p not in [2,3,5,7]:
		raise ValueError()
	n = "".join(( str(d) for d in base(n, p) )) # base p string
	return cumsum(n, p)

assert main(7) == 28
assert main(100) == 2361
print(main(10**9))