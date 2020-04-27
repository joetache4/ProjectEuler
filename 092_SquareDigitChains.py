"""

A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.

For example,

44 → 32 → 13 → 10 → 1 → 1
85 → 89 → 145 → 42 → 20 → 4 → 16 → 37 → 58 → 89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?

ans: 8581146
"""

mem = dict()

def test(n):

	v = []
	while True:
	
		mem[n] = v	
		n = sum(( int(d)**2 for d in str(n) ))
		
		if n in mem and len(mem[n]) > 0:
			v.append(mem[n][0])
			break
		if n == 1:
			v.append(0)
			break
		if n == 89:
			v.append(1)
			break

for n in range(1, 10**7):
	test(n)
	
print(sum(( v[0] for v in mem.values() )))