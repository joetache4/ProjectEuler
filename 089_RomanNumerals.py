"""
For a number written in Roman numerals to be considered valid there are basic rules which must be followed. Even though the rules allow some numbers to be expressed in more than one way there is always a "best" way of writing a particular number.

For example, it would appear that there are at least six ways of writing the number sixteen:

IIIIIIIIIIIIIIII
VIIIIIIIIIII
VVIIIIII
XIIIIII
VVVI
XVI

However, according to the rules only XIIIIII and XVI are valid, and the last example is considered to be the most efficient, as it uses the least number of numerals.

The 11K text file, roman.txt (right click and 'Save Link/Target As...'), contains one thousand numbers written in valid, but not necessarily minimal, Roman numerals; see About... Roman Numerals for the definitive rules for this problem.

Find the number of characters saved by writing each of these in their minimal form.

Note: You can assume that all the Roman numerals in the file contain no more than four consecutive identical units.


ans: 743
"""

from _data.p089 import get_data

numerals = get_data()

def to_number(numeral):
	val = 0
	prev = 1000	
	for n in numeral:
		v = {"I":1, "V":5, "X":10, "L":50, "C":100, "D":500, "M":1000}[n]
		if prev < v:
			val -= prev
			v = (v - prev)
		prev = v
		val += v
	return val

assert to_number("I") == 1
assert to_number("VIIII") == 9
assert to_number("IX") == 9
assert to_number("MIX") == 1009
assert to_number("XLIX") == 49
assert to_number("MCCCCCCVI") == 1606
assert to_number("MDCVI") == 1606

def to_numeral(n):
	num = "M" * (n//1000)
	
	n %= 1000
	d = n//100
	if d == 0:
		pass
	elif d == 1:
		num += "C"
	elif d == 2:
		num += "CC"
	elif d == 3:
		num += "CCC"
	elif d == 4:
		num += "CD"
	elif d == 5:
		num += "D"
	elif d == 6:
		num += "DC"
	elif d == 7:
		num += "DCC"
	elif d == 8:
		num += "DCCC"
	elif d == 9:
		num += "CM"
	
	n %= 100
	d = n//10
	if d == 0:
		pass
	elif d == 1:
		num += "X"
	elif d == 2:
		num += "XX"
	elif d == 3:
		num += "XXX"
	elif d == 4:
		num += "XL"
	elif d == 5:
		num += "L"
	elif d == 6:
		num += "LX"
	elif d == 7:
		num += "LXX"
	elif d == 8:
		num += "LXXX"
	elif d == 9:
		num += "XC"
	
	n %= 10
	d = n
	if d == 0:
		pass
	elif d == 1:
		num += "I"
	elif d == 2:
		num += "II"
	elif d == 3:
		num += "III"
	elif d == 4:
		num += "IV"
	elif d == 5:
		num += "V"
	elif d == 6:
		num += "VI"
	elif d == 7:
		num += "VII"
	elif d == 8:
		num += "VIII"
	elif d == 9:
		num += "IX"
	
	return num


assert to_numeral(1606) == "MDCVI"

print(sum(( len(n) - len(to_numeral(to_number(n))) for n in numerals )))