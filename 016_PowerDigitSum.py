"""
2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000?

ans: 1366
"""

base = 2
pow  = 1000

sum = 0
for digit in str(base**pow):
	sum += int(digit)
	
print(sum)