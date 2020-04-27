"""
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

ans: 232792560
"""

from functools import reduce
from lib.num import lcm

target = 20

print(reduce(lcm, range(2, target)))