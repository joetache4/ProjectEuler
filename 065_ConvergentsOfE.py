"""
Find the sum of digits in the numerator of the 100th convergent of the continued fraction for e.


ans: 272
"""

e = [2,1,2]

k = 4 
while len(e) < 100:
	e.append(1)
	e.append(1)
	e.append(k)
	k += 2
e = e[:100]

numer = 1
denom = e[99]

for d in e[:99][::-1]:
	numer, denom = denom, numer + d*denom
numer, denom = denom, numer

# no need to take GCD

print(sum(( int(d) for d in str(numer) )))