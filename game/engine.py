import random
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])

RANKS = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
SUITS = ['h', 'd', 'c', 's']

class Player():
    def __init__(self, hole_cards=None, stack=100):
        if hole_cards is not None:
            self.hole_cards = hole_cards
        else:
            self.hole_cards = []
        self.stack = stack

class Deck():

    def __init__(self):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]

        # We shuffle cards so that we can pop cards from the end of the list
        # and still have randomly ordered cards.
        random.shuffle(self.cards)

    def draw(self):
        card = self.cards.pop()
        return card

    def __len__(self):
        return len(self.cards)

class Game():

    def __init__(self, players, button_position=0):
        self.players = tuple(Player([], 100) for index in range(players))
        self.deck = Deck()
        self.button_position = button_position
        self.pot = 0
        self.board = []

    def deal(self):
        for player in self.players:
            player.hole_cards = self.deck.draw(), self.deck.draw()

    def post_blinds(self):
        sb_position = (self.button_position+1) % len(self.players)
        bb_position = (self.button_position+2) % len(self.players)

        self.pot += 1.5

        self.players[sb_position].stack -= 0.5
        self.players[bb_position].stack -= 1

    def flop(self):
        self.board = [self.deck.draw() for card in range(3)]

    def turn(self):
        self.board.append(self.deck.draw())

    def river(self):
        self.board.append(self.deck.draw())