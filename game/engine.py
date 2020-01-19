import random
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])
Player = namedtuple('Player', ['hole_cards', 'stack'])

RANKS = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
SUITS = ['h', 'd', 'c', 's']

class Deck():

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]

    def draw(self):
        card = random.choice(self.cards)
        return card

class Game():
    def __init__(self, players):
        self.players = tuple(Player([], 100) for index in range(players))
        self.deck = Deck()