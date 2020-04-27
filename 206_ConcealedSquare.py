"""
Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0,
where each “_” is a single digit.

ans: 1389019170
"""

from math import sqrt

def main():
	for a in [0,1,2,3,4,5,6,7,8,9]:
		for b in [0,1,2,3,4,5,6,7,8,9]:
			for c in [0,1,2,3,4,5,6,7,8,9]:
				for d in [0,1,2,3,4,5,6,7,8,9]:
					for e in [0,1,2,3,4,5,6,7,8,9]:
						for f in [0,1,2,3,4,5,6,7,8,9]:
							for g in [0,1,2,3,4,5,6,7,8,9]:
								for h in [0,1,2,3,4,5,6,7,8,9]:
									for i in [0]:
										num = 0
										for j in [1,a,2,b,3,c,4,d,5,e,6,f,7,g,8,h,9,i]:
											num = 10*(num + j)
										sqrt_num = int(sqrt(num))
										if num == sqrt_num**2:
											print(sqrt(num))
											return
main()