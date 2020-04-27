"""
The proper divisors of a number are all the divisors excluding the number itself. For example, the proper divisors of 28 are 1, 2, 4, 7, and 14. As the sum of these divisors is equal to 28, we call it a perfect number.

Interestingly the sum of the proper divisors of 220 is 284 and the sum of the proper divisors of 284 is 220, forming a chain of two numbers. For this reason, 220 and 284 are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with 12496, we form a chain of five numbers:

12496 → 14288 → 15472 → 14536 → 14264 (→ 12496 → ...)

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element exceeding one million.


ans: 14316
"""

max_val = 10**6

div = [[1] for x in range(max_val+1)]

div[0] = [0]
div[1] = [0]

for a in range(2, max_val//2+1):
	for b in range(2*a, max_val+1, a):
		div[b].append(a)

assert div[24] == [1,2,3,4,6,8,12]
assert div[28] == [1,2,4,7,14]

for i in range(len(div)):
	div[i] = sum(div[i])

assert div[28] == 28
assert div[220] == 284
assert div[284] == 220

chain_len = {}

def get_chain_len(start):
	if start in chain_len:
		return
	visited = []	
	n = start
	while True:
		visited.append(n)
		n = div[n]		
		if n > max_val or n == 0:
			# faster to not do this
			# for m in visited:
			#	chain_len[m] = -1
			break
		elif n == start:
			for m in visited:
				chain_len[m] = len(visited)
			break
		elif n in visited:
			break

for i in range(len(div)):
	get_chain_len(i)

assert 7 not in chain_len
assert chain_len[28] == 1
assert chain_len[220] == 2
assert chain_len[284] == 2
assert chain_len[12496] == 5
assert chain_len[14288] == 5
assert chain_len[15472] == 5
assert chain_len[14536] == 5
assert chain_len[14264] == 5

longest = max(( (length,-start) for start,length in chain_len.items() ))
print(-longest[1])