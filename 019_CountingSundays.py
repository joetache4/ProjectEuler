"""
You are given the following information, but you may prefer to do some research for yourself.

    1 Jan 1900 was a Monday.
    Thirty days has September,
    April, June and November.
    All the rest have thirty-one,
    Saving February alone,
    Which has twenty-eight, rain or shine.
    And on leap years, twenty-nine.
    A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

ans: 171
"""

# set to day of week for 1 Jan 1901 (Tuesday)
dow = 2

def no_days(month, year):
	if month in [0,2,4,6,7,9,11]:
		return 31
	elif month in [3,5,8,10]:
		return 30
	elif year % 400 == 0:
		return 29
	elif year % 100 == 0:
		return 28
	elif year % 4 == 0:
		return 29
	else:
		return 28

sum = 0
for y in range(1901, 2001):
	for m in range(0, 12):
		if dow == 0:	
			sum += 1
		dow = (dow + no_days(m, y)) % 7
print(sum)