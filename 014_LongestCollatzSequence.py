"""
The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.

ans: 837799 has collatz length 525
"""

upto = 1000000

def collatz_length(n):
	length = 1
	while n != 1:
		if n%2 == 0:
			n = n/2
		else:
			n = 3*n + 1
		length += 1
	return length

memmory = dict()
def collatz_length_r(n):
	if n == 1:
		return 1
	if n in memmory:
		return memmory[n]
	
	length = 1
	if n%2 == 0:
		length += collatz_length_r(n/2)
	else:
		length += collatz_length_r(3*n + 1)
		
	if n not in memmory:
		memmory[n] = length
	return length
	
def test():
	print("Beginning test")
	for k in range(1,100):
		assert collatz_length(k) == collatz_length_r(k)
	print("Test complete")
# test()
	
max   = -1
max_n = -1
for n in range (1, upto):
	length = collatz_length_r(n)
	if length > max:
		max = length
		max_n = n

print("{} has collatz length {}".format(max_n, max))