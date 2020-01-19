import random
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])
RANKS = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
SUITS = ['h', 'd', 'c', 's']

class Deck():

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]

    def draw(self):
        card = random.choice(self.cards)
        return card

