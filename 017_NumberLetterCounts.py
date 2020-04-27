"""
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.


ans: 21124
"""

def ones(n):
	return {
		0: 0,
		1: len("one"),
		2: len("two"),
		3: len("three"),
		4: len("four"),
		5: len("five"),
		6: len("six"),
		7: len("seven"),
		8: len("eight"),
		9: len("nine")
	}[n]
	
def tens(n):
	if n < 10:
		return ones(n)
	elif n < 20:
		return {
			10: len("ten"),
			11: len("eleven"),
			12: len("twelve"),
			13: len("thirteen"),
			14: len("fourteen"),
			15: len("fifteen"),
			16: len("sixteen"),
			17: len("seventeen"),
			18: len("eighteen"),
			19: len("nineteen")
		}[n]
	else:
		return {
			2: len("twenty"),
			3: len("thirty"),
			4: len("forty"),
			5: len("fifty"),
			6: len("sixty"),
			7: len("seventy"),
			8: len("eighty"),
			9: len("ninety")
		}[int(n / 10)] + ones(n % 10)

# works for 1 to 999
def word_length(n):
	a = int(n / 100) # 100's
	b =     n % 100  #  10's
		
	if a == 0 and b != 0:
		return tens(b)
	elif a != 0 and b == 0:
		return ones(a) + len("hundred")
	else:
		return ones(a) + len("hundredand") + tens(b)
		
def test():
	assert word_length(1)   == len("one")
	assert word_length(12)  == len("twelve")
	assert word_length(20)  == len("twenty")
	assert word_length(23)  == len("twentythree")
	assert word_length(313) == len("threehundredandthirteen")
	assert word_length(500) == len("fivehundred")
	assert word_length(802) == len("eighthundredandtwo")
	
test()

sum = 0
for n in range(1, 1000):
	sum += word_length(n)
sum += len("onethousand")

print(sum)