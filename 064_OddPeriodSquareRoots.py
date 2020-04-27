"""
How many continued fractions of sqrt(n) for n≤10000 have an odd period?

ans: 1322
"""

# https://en.wikipedia.org/wiki/Periodic_continued_fraction#Canonical_form_and_repetend

from math import sqrt

def nonsquare(m):
	n = 2
	while n < m:
		if n != int(sqrt(n))**2:
			yield n
		n += 1

def frac_len(n):
	m = [0]
	d = [1]
	a = [int(math.sqrt(n))]
	while True:
		m_new = d[-1]*a[-1] - m[-1]
		d_new = (n - m_new**2)//d[-1]
		a_new = int((a[0]+m_new)/d_new)
		m.append(m_new)
		d.append(d_new)
		a.append(a_new)
		if a_new == 2*a[0]:
			break
	return len(a) - 1

print(sum(( 1 for n in nonsquare(10001) if frac_len(n) % 2 == 1 )))