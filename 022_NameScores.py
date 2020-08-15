"""
Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?

ans: 871198282
"""

from _data.p022 import get_data

def score(name):
	return sum([ord(x)-96 for x in name.lower()])

names = get_data()
names.sort()	

total = 0
for name, pos in zip(names, range(1, len(names)+1)):
	total += score(name) * pos

print(total)