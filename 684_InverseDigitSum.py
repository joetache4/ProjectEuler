# 684 Inverse Digit Sum

# Solution by Joe Tacheron
# 17 May 2020

# Answer  : 922058210
# Run time: 0.1s

"""
Define s(n) to be the smallest number that has a digit sum of n. For example s(10)=19.
Let S(k)=∑n,1,k,s(n). You are given S(20)=1074.

Further let fi be the Fibonacci sequence defined by f[0]=0,f[1]=1 and f[i]=f[i−2]+f[i−1] for all i≥2.

Find ∑i,2,90,S(f[i]). Give your answer modulo 1000000007.
"""

"""
Solution Method

S is built up from previous two results, similar to the method of calculating fibanocci numbers.

The key is the shift() method, which takes a cumulative S(n) and returns S(n + offset) - S(offset).

This is used to calculate S(f[n]) = S(f[n-1] + f[n-2]).
"""

from random import randint
from lib.num import fibonacci, mod_pow

mod = 1000000007

# Returns the smallest int with digit sum n.
# Such an int will be all 9's, possibly except for the most siginifant digit, which is n%9.
def s(n):
	#return (1 + n%9) * 10**(n//9) - 1
	return ( (1 + n%9) * mod_pow(10, n//9, mod) - 1 ) % mod

# Also see the S() method to understand why shift() works.
def shift(S, n, offset):
	# Every s() ends with -1 in its calculation. 
	# Temporarily add them back.
	S += n
	# Incrementally shift until the remaining offset if a multiple of 9.
	for i in range(offset%9):
		S -= s(  i+1)
		S += s(n+i+1)
	# Each multiple of 9 adds a '9' digit to the end of every s().
	# But since we added 1 to each s() above, I instead multiply by 10.
	S *= mod_pow(10, offset//9, mod)
	# Subtract away the temporary 1's.
	S -= n
	return S % mod

fib = [0, 1]
mem = [0, 1]
for i,f0 in enumerate(fibonacci()):
	if i in [0,1]:
		continue
	elif i > 90:
		break
	
	S1     = mem[-1]
	S2     = mem[-2]
	offset = fib[-1]
	f2     = fib[-2]
	
	S0     = (S1 + shift(S2, f2, offset)) % mod
	
	fib.append(f0)
	mem.append(S0)

print(sum(mem[2:]) % mod)


'''
def S(n):
	ans  = (2 + n%9)*(1 + n%9)//2 * mod_pow(10, (n//9), mod)
	ans += sum( 45*mod_pow(10, i, mod) for i in range(n//9) ) # mod_pow is slow for small exponents.
	ans -= (n + 1)
	return ans % mod

def s_test(n):
	return (1 + n%9) * 10**(n//9) - 1
	
def S_test(n):
	return sum( s_test(m) for m in range(1, n+1) )
'''