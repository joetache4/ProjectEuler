"""
The sum of the squares of the first ten natural numbers is,
1^2 + 2^2 + ... + 10^2 = 385

The square of the sum of the first ten natural numbers is,
(1 + 2 + ... + 10)^2 = 55^2 = 3025

Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 − 385 = 2640.

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.


ans: 25164150
"""

n = 100

square_of_sum = int((n * (n+1) / 2)**2)
sum_of_squares = 0

for k in range(1, n+1):
	sum_of_squares += k*k

print(square_of_sum - sum_of_squares)