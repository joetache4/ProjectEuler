"""
Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a 20×20 grid?

ans: 137846528820
"""

from lib.num import factorial

height = 20
width  = 20

# the number of permutations of 20 H's and 20 V's
ans = factorial(height + width)/(factorial(height)*factorial(width))
ans = int(ans)

print(ans) 