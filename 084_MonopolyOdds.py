"""

In the game, Monopoly, the standard board is set up in the following way:

		GO	A1	CC1	A2	T1	R1	B1	CH1	B2	B3	JAIL
		H2										C1
		T2										U1
		H1										C2
		CH3										C3
		R4										R2
		G3										D1
		CC3										CC2
		G2										D2
		G1										D3
		G2J	F3	U2	F2	F1	R3	E3	E2	CH2	E1	FP 

A player starts on the GO square and adds the scores on two 6-sided dice to determine the number of squares they advance in a clockwise direction. Without any further rules we would expect to visit each square with equal probability: 2.5%. However, landing on G2J (Go To Jail), CC (community chest), and CH (chance) changes this distribution.

In addition to G2J, and one card from each of CC and CH, that orders the player to go directly to jail, if a player rolls three consecutive doubles, they do not advance the result of their 3rd roll. Instead they proceed directly to jail.

At the beginning of the game, the CC and CH cards are shuffled. When a player lands on CC or CH they take a card from the top of the respective pile and, after following the instructions, it is returned to the bottom of the pile. There are sixteen cards in each pile, but for the purpose of this problem we are only concerned with cards that order a movement; any instruction not concerned with movement will be ignored and the player will remain on the CC/CH square.

    Community Chest (2/16 cards):
        Advance to GO
        Go to JAIL
    Chance (10/16 cards):
        Advance to GO
        Go to JAIL
        Go to C1
        Go to E3
        Go to H2
        Go to R1
        Go to next R (railway company)
        Go to next R
        Go to next U (utility company)
        Go back 3 squares.

The heart of this problem concerns the likelihood of visiting a particular square. That is, the probability of finishing at that square after a roll. For this reason it should be clear that, with the exception of G2J for which the probability of finishing on it is zero, the CH squares will have the lowest probabilities, as 5/8 request a movement to another square, and it is the final square that the player finishes at on each roll that we are interested in. We shall make no distinction between "Just Visiting" and being sent to JAIL, and we shall also ignore the rule about requiring a double to "get out of jail", assuming that they pay to get out on their next turn.

By starting at GO and numbering the squares sequentially from 00 to 39 we can concatenate these two-digit numbers to produce strings that correspond with sets of squares.

Statistically it can be shown that the three most popular squares, in order, are JAIL (6.24%) = Square 10, E3 (3.18%) = Square 24, and GO (3.09%) = Square 00. So these three most popular squares can be listed with the six-digit modal string: 102400.

If, instead of using two 6-sided dice, two 4-sided dice are used, find the six-digit modal string.


ans: 101524
"""


# Simulate a bunch of moves

from random import randint, shuffle
from collections import deque, Counter

roll4 = lambda: (randint(1,4), randint(1,4))
roll6 = lambda: (randint(1,6), randint(1,6))

squares = ["GO", "A1", "CC1", "A2", "T1", "R1", "B1", "CH1", "B2", "B3", "JAIL", "C1", "U1", "C2", "C3", "R2", "D1", "CC2", "D2", "D3", "FP", "E1", "CH2", "E2", "E3", "R3", "F1", "F2", "U2", "F3", "G2J", "G1", "G2", "CC3", "G3", "R4", "CH3", "H1", "T2", "H2"]

GO   = squares.index("GO")
JAIL = squares.index("JAIL")
G2J  = squares.index("G2J")
C1   = squares.index("C1")
E3   = squares.index("E3")
H2   = squares.index("H2")
R1   = squares.index("R1")
R2   = squares.index("R2")
R3   = squares.index("R3")
R4   = squares.index("R4")
U1   = squares.index("U1")
U2   = squares.index("U2")
CC1  = squares.index("CC1")
CC2  = squares.index("CC2")
CC3  = squares.index("CC3")
CH1  = squares.index("CH1")
CH2  = squares.index("CH2")
CH3  = squares.index("CH3")

cc_cards = list(range(16))
shuffle(cc_cards)
cc_cards = deque(cc_cards)
def cc():
	c = cc_cards.popleft()
	cc_cards.append(c)
	if c == 0:
		return GO
	elif c == 1:
		return JAIL
	return None

ch_cards = list(range(16))
shuffle(ch_cards)
ch_cards = deque(ch_cards)
def ch():
	c = cc_cards.popleft()
	cc_cards.append(c)
	try:
		return {0:GO, 1:JAIL, 2:C1, 3:E3, 4:H2, 5:R1, 6:-1, 7:-1, 8:-2, 9:-3}[c]
	except KeyError:
		return None

rolls = []
def next(pos):
	roll = roll4()
	
	if len(rolls) == 3:
		rolls.pop(0)
	rolls.append(roll)
	
	if len(rolls) == 3 and all(( a == b for a,b in rolls )):
		pos = JAIL
		rolls.pop() # TODO reset rolls after going to jail ?
		rolls.pop()
		rolls.pop()
	else:
		pos = (pos + sum(roll)) % len(squares)
	
		if pos == G2J: # G2J
			 pos = JAIL
		elif pos in [CC1, CC2, CC3]: #cc
			cc_card = cc()
			if cc_card is not None:
				pos = cc_card
		elif pos in [CH1, CH2, CH3]: #ch
			ch_card = ch()
			if ch_card is None:
				pass
			elif ch_card >= 0:
				pos = ch_card
			elif ch_card == -1: # next railway
				pos = {CH1:R2, CH2:R3, CH3:R1}[pos]
			elif ch_card == -2: # next utility
				pos = {CH1:U1, CH2:U2, CH3:U1}[pos]
			elif ch_card == -3: # back 3
				pos -= 3
	
	return pos

pos    = 0
totals = Counter()
for i in range(10**6):
	pos = next(pos)	
	totals[pos] += 1

ans = sorted(totals, key = lambda i: totals[i], reverse = True)[:3]
ans = "".join( str(n) for n in ans )
print(ans)