"""
Comparing two numbers written in index form like 2^11 and 3^7 is not difficult, as any calculator would confirm that 2^11 = 2048 < 3^7 = 2187.

However, confirming that 632382^518061 > 519432^525806 would be much more difficult, as both numbers contain over three million digits.

Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file containing one thousand lines with a base/exponent pair on each line, determine which line number has the greatest numerical value.

NOTE: The first two lines in the file represent the numbers in the example given above.

ans: 709
"""

from math import log

from _data.p099 import get_data

data = get_data()

max, max_i = data[0], 0
for i, a in enumerate(data):
	if a[1] > max[1] * log(max[0], a[0]):
		max = a
		max_i = i

print(max_i + 1)