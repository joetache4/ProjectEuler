"""
In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

    High Card: Highest value card.
    One Pair: Two cards of the same value.
    Two Pairs: Two different pairs.
    Three of a Kind: Three cards of the same value.
    Straight: All cards are consecutive values.
    Flush: All cards of the same suit.
    Full House: Three of a kind and a pair.
    Four of a Kind: Four cards of the same value.
    Straight Flush: All cards are consecutive values of same suit.
    Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:
Hand	 	Player 1	 	Player 2	 	Winner
1	 	5H 5C 6S 7S KD
Pair of Fives
	 	2C 3S 8S 8D TD
Pair of Eights
	 	Player 2
2	 	5D 8C 9S JS AC
Highest card Ace
	 	2C 5C 7D 8S QH
Highest card Queen
	 	Player 1
3	 	2D 9C AS AH AC
Three Aces
	 	3D 6D 7D TD QD
Flush with Diamonds
	 	Player 2
4	 	4D 6S 9H QH QC
Pair of Queens
Highest card Nine
	 	3D 6D 7H QD QS
Pair of Queens
Highest card Seven
	 	Player 1
5	 	2H 2D 4C 4D 4S
Full House
With Three Fours
	 	3C 3D 3S 9S 9D
Full House
with Three Threes
	 	Player 1

The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?

ans: 376
"""

from _data.p054 import get_data

tr  = lambda s, a, b: s.translate(str.maketrans(a,b))

hex = lambda int: "{:X}".format(int)

######################################################################################################
# assumes converted ranks to ints & sorted high to low

royal = lambda cards: "900" if all(cards[i][0] == 14 - i for i in range(5)) and flush(cards) else ""

sflsh = lambda cards: "800" if strat(cards) and flush(cards) else ""

four  = lambda cards: f"7{hex(cars[2][0])}0" if cards[0][0] == cards[3][0] or \
												cards[1][0] == cards[4][0] else ""

full  = lambda cards: f"6{hex(cards[0][0])}{hex(cards[4][0])}" if cards[0][0] == cards[2][0] and \
																  cards[3][0] == cards[4][0] else \
					  f"6{hex(cards[4][0])}{hex(cards[0][0])}" if cards[0][0] == cards[1][0] and \
																  cards[2][0] == cards[4][0] else ""

strat = lambda cards: "500" if all(cards[i][0] == cards[i+1][0] + 1 for i in range(4)) else ""

flush = lambda cards: "400" if all(cards[i][1] == cards[i+1][1] for i in range(4)) else ""

three = lambda cards: f"3{hex(cards[2][0])}0" if cards[0][0] == cards[2][0] or \
												 cards[1][0] == cards[3][0] or \
												 cards[2][0] == cards[4][0] else ""

tpair = lambda cards: (cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0]) or \
					  (cards[0][0] == cards[1][0] and cards[3][0] == cards[4][0]) or \
					  (cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0])

def tpair(cards):
	is_tpair = (cards[0][0] == cards[1][0] and cards[2][0] == cards[3][0]) or \
	           (cards[0][0] == cards[1][0] and cards[3][0] == cards[4][0]) or \
	           (cards[1][0] == cards[2][0] and cards[3][0] == cards[4][0])
	if is_tpair:
		p1 = hex(cards[1][0])
		p2 = hex(cards[3][0])
		if p1 > p2:
			return "2" + p1 + p2
		else:
			return "2" + p2 + p1
	else:
		return ""

pair  = lambda cards: f"1{hex(cards[1][0])}0" if cards[0][0] == cards[1][0] else \
					  f"1{hex(cards[2][0])}0" if cards[1][0] == cards[2][0] else \
					  f"1{hex(cards[3][0])}0" if cards[2][0] == cards[3][0] else \
					  f"1{hex(cards[4][0])}0" if cards[3][0] == cards[4][0] else ""

high  = lambda cards: "000"

######################################################################################################

values = lambda cards: [(int(tr(card[0], "TJQKA", "ABCDE"), 16), card[1]) for card in cards]

rank_order = lambda cards: "".join([hex(card[0]) for card in cards])

def score(cards):
	cards = values(cards)
	cards.sort()
	cards = cards[::-1]
	
	for type in [royal, sflsh, four, full, strat, flush, three, tpair, pair, high]:
		t = type(cards)
		if t:
			return t + rank_order(cards)
	raise Exception()

winner = lambda cards: score(cards[:5]) > score(cards[5:])

rounds = get_data()

print(sum(( winner(cards) for cards in rounds )))