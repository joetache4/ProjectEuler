"""
Largest prime factor of 600851475143

ans: 6857
"""

from lib.num import factor

num = 600851475143

factors = factor(num)
print(factors[-1])