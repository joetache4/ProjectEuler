'''
Each of the six faces on a cube has a different digit (0 to 9) written on it; the same is done to a second cube. By placing the two cubes side-by-side in different positions we can form a variety of 2-digit numbers.

For example, the square number 64 could be formed:

In fact, by carefully choosing the digits on both cubes it is possible to display all of the square numbers below one-hundred: 01, 04, 09, 16, 25, 36, 49, 64, and 81.

For example, one way this can be achieved is by placing {0, 5, 6, 7, 8, 9} on one cube and {1, 2, 3, 4, 8, 9} on the other cube.

However, for this problem we shall allow the 6 or 9 to be turned upside-down so that an arrangement like {0, 5, 6, 7, 8, 9} and {1, 2, 3, 4, 6, 7} allows for all nine square numbers to be displayed; otherwise it would be impossible to obtain 09.

In determining a distinct arrangement we are interested in the digits on each cube, not the order.

{1, 2, 3, 4, 5, 6} is equivalent to {3, 6, 4, 1, 2, 5}
{1, 2, 3, 4, 5, 6} is distinct from {1, 2, 3, 4, 5, 9}

But because we are allowing 6 and 9 to be reversed, the two distinct sets in the last example both represent the extended set {1, 2, 3, 4, 5, 6, 9} for the purpose of forming 2-digit numbers.

How many distinct arrangements of the two cubes allow for all of the square numbers to be displayed?


ans: 1217
'''

from lib.list import subsets

def pair_represented(a, b, p):
	return (p[0] in a and p[1] in b) or (p[0] in b and p[1] in a)

def good_dice(a, b):
	pairs_all = [(0,1),(0,4),(2,5),(8,1)]
	pairs_any = [[(0,9),(0,6)], [(1,6),(1,9)], [(3,6),(3,9)], [(4,9),(4,6)], [(6,4),(9,4)]]
	
	if any(( not pair_represented(a,b,p) for p in pairs_all )):
		return False
	
	for either in pairs_any:
		if all(( not pair_represented(a,b,p) for p in either )):
			return False
	
	return True

nums  = list(range(10))
count = 0

for a in subsets(nums, min_size = 6, max_size = 6):
	for b in subsets(nums, min_size = 6, max_size = 6):
		if good_dice(a,b):
			count += 1

print(count//2) # the order of the dice does not matter