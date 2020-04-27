"""
A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

    1/2	= 	0.5
    1/3	= 	0.(3)
    1/4	= 	0.25
    1/5	= 	0.2
    1/6	= 	0.1(6)
    1/7	= 	0.(142857)
    1/8	= 	0.125
    1/9	= 	0.(1)
    1/10	= 	0.1 

Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

ans: 983

"""

def cycle_len(d):
	n = 1
	visited = [1]
	
	while True:
		if n < d:
			n *= 10
		n %= d
		if n == 0:
			return 0
		if n in visited:
			return len(visited) - visited.index(n)
		else:
			visited.append(n)

assert cycle_len(2) == 0
assert cycle_len(3) == 1
assert cycle_len(7) == 6
assert cycle_len(17) == 16
assert cycle_len(101) == 4
assert cycle_len(15) == 1

assert max(range(2, 10), key = lambda i: cycle_len(i)) == 7

print(max(range(2, 1000), key = lambda i: cycle_len(i)))