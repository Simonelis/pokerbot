import random
from collections import namedtuple

Card = namedtuple("Card", ["rank", "suit"])

RANKS = [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
SUITS = ["h", "d", "c", "s"]


def is_straight(hand):
    """hand is a collection of 7 cards.
    Returns highest straight"""
    ranks = [card.rank for card in hand]
    ranks = list(sorted(ranks, reverse=True))

    if ranks[0] == 14:
        ranks.append(1)
    straight_counter = 1
    previous_rank = ranks[0]
    straight_rank = ranks[0]
    for rank in ranks[1:]:
        if previous_rank - 1 == rank:
            straight_counter += 1
        elif previous_rank == rank:
            straight_counter += 0
        else:
            straight_counter = 1
            straight_rank = rank
        if straight_counter == 5:
            return straight_rank
        previous_rank = rank
    return False


def is_flush(hand):
    suits = [card.suit for card in hand]
    suits_set = set(suits)
    if len(suits_set) > 3:
        return False
    for suit in suits_set:
        if suits.count(suit) > 4:
            ranks = [card.rank for card in hand if card.suit == suit]
            return max(ranks)
    return False


def is_straight_flush(hand):
    flush = is_flush(hand)
    if flush:
        straight = is_straight(hand)
        if flush == straight:
            return flush
    return False


def is_quads(hand):
    ranks = [card.rank for card in hand]
    ranks_set = set(ranks)
    if len(ranks_set) > 4:
        return False
    for rank in ranks_set:
        if ranks.count(rank) == 4:
            ranks_set.remove(rank)
            return (rank, max(ranks_set))
    return False


def hand_strength(hand):
    is_straight_flush(hand)
    is_quads(hand)
    is_flush(hand)
    is_straight(hand)
    return 1


class Player:
    def __init__(self, hole_cards=None, stack=100):
        if hole_cards is not None:
            self.hole_cards = hole_cards
        else:
            self.hole_cards = []
        self.stack = stack


class Deck:
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


class Game:
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
        sb_position = (self.button_position + 1) % len(self.players)
        bb_position = (self.button_position + 2) % len(self.players)

        self.pot += 1.5

        self.players[sb_position].stack -= 0.5
        self.players[bb_position].stack -= 1

    def flop(self):
        """Draws three cards from the deck and adds them the board"""
        self.board = [self.deck.draw() for card in range(3)]

    def turn(self):
        """Draws one card from the deck and adds it to the board"""
        self.board.append(self.deck.draw())

    def river(self):
        """Draws one card from the deck and adds it to the board"""
        self.board.append(self.deck.draw())

    def get_player_hand(self, player):
        hole_cards = self.players[player].hole_cards
        player_hand = list(hole_cards) + list(self.board)
        return player_hand
