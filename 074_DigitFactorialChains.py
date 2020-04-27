"""
The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:

1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169; it turns out that there are only three such loops that exist:

169 → 363601 → 1454 → 169
871 → 45361 → 871
872 → 45362 → 872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,

69 → 363600 → 1454 → 169 → 363601 (→ 1454)
78 → 45360 → 871 → 45361 (→ 871)
540 → 145 (→ 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain with a starting number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?


ans: 402
"""

def dig_fac(n, _map = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]):
	ans = 0
	while n > 9:
		ans += _map[n % 10]
		n //= 10
	ans += _map[n]
	return ans

chain_len = {} 

def start(n, visited = None):
	if visited is None:
		visited = []
	
	if n in chain_len:
		a = chain_len[n]
		b = len(visited)
		for i in range(b-1, -1, -1):
			chain_len[visited[i]] = a + b - i

	elif n in visited:
		a = len(visited)
		b = visited.index(n)
		for i in range(a-1, b-1, -1):
			chain_len[visited[i]] = a - b
		for i in range(b-1, -1, -1):
			chain_len[visited[i]] = a - i
	
	else:
		visited.append(n)
		start(dig_fac(n), visited)

for i in range(10**6):
	start(i)

print(sum(( 1 for k,v in chain_len.items() if v == 60 )))