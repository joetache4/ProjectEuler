# 686 Powers of Two

# Solution by Joe Tacheron
# 17 May 2020

# Answer  : 193060223
# Run time: 157s

"""
2^7=128 is the first power of two whose leading digits are "12".
The next power of two whose leading digits are "12" is 280.

Define p(L,n) to be the nth-smallest value of j such that the base 10 representation of 2^j begins with the digits of L. So p(12,1)=7 and p(12,2)=80.

You are also given that p(123,45)=12710.

Find p(123,678910).
"""

"""
Solution Method

Solve for m in 10^m = 2^n. So m = n*log(2,10).

Let x be the leading digits. 
Let d be length(str(x)) - 1 (the exponent in the scientific notation of x).

Then, x * 10^(floor(m)-d) <= 2^n <= (x+1) * 10^(floor(m)-d).
Take log_10 of all sides to get 
floor(m) + log(x) - d <= m <= floor(m) + log(x+1) - d.

Iterate n and see which fulfill the above inequalities.
"""

from math import log, floor

x = 123
y = 678910

M = lambda n: n*log(2, 10)
D = lambda d: floor(log(d, 10))

d    = D(x)
log0 = log(x,   10) - d
log1 = log(x+1, 10) - d

n = 0
while True:
	m  = M(n)
	fm = floor(m)	
	if fm + log0 <= m and m <= fm + log1:
		y -= 1
		if y == 0:
			break
	n += 1

print(n)