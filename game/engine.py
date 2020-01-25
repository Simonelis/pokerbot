from collections import namedtuple
import random

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
    suits = [card.suit for card in hand]
    suits_set = set(suits)

    for suit in suits_set:
        hand_suit = [card for card in hand if card.suit == suit]
        straight = is_straight(hand_suit)
        if straight:
            return (1, straight)
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


def is_full_house_trips_two_pair_high_card(hand):
    ranks = [card.rank for card in hand]
    counts = {}
    for rank in ranks:
        if rank in counts:
            counts[rank] += 1
        else:
            counts[rank] = 1
    trips = []
    pairs = []
    singles = []
    for rank, count in counts.items():
        if count == 3:
            trips.append(rank)
        elif count == 2:
            pairs.append(rank)
        else:
            singles.append(rank)
    trips = list(sorted(trips, reverse=True))
    pairs = list(sorted(pairs, reverse=True))
    singles = list(sorted(singles, reverse=True))

    if len(trips) >= 1:
        if len(pairs) >= 1:
            return (3, (max(trips), max(pairs)))
        elif len(trips) == 2:
            return (3, (max(trips), min(trips)))
        else:
            return (6, (max(trips),) + tuple(singles[:2]))
    elif len(pairs) == 3:
        return (7, (pairs[0], pairs[1], max(pairs[2], max(singles))))
    elif len(pairs) == 2:
        return (7, (max(pairs), min(pairs), max(singles)))
    elif len(pairs) == 1:
        return (8, (pairs[0],) + tuple(singles[:3]))
    return (9, tuple(singles[:5]))


def hand_strength(hand):
    quads_result = is_quads(hand)
    flush_result = is_flush(hand)
    straight_result = is_straight(hand)

    # straight flush
    if flush_result and straight_result:
        straight_flush_result = is_straight_flush(hand)
        if straight_flush_result:
            return (1, straight_flush_result)
    # quads
    if quads_result:
        return (2, quads_result)

    # the rest with ranks
    the_rest = is_full_house_trips_two_pair_high_card(hand)
    if the_rest[0] == 3:
        return the_rest
    # flush
    if flush_result:
        return (4, (flush_result,))
    # straight
    if straight_result:
        return (5, (straight_result,))

    return the_rest


def winning_hand(hand1, hand2):
    """Returns index of winning hand. If the hands are equal
    in strength, returns -1"""
    strength1 = hand_strength(hand1)
    strength2 = hand_strength(hand2)
    # The strengths seem to be inverted here, but they are
    # correct, because the strongest hand is "1" - straight flush.
    if strength1[0] < strength2[0]:
        return 0
    elif strength1[0] > strength2[0]:
        return 1
    else:
        for ind1, ind2 in zip(strength1[1], strength2[1]):
            if ind1 > ind2:
                return 0
            elif ind1 < ind2:
                return 1
            else:
                continue
    return -1


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
    def __init__(self, players=None, button_position=0):
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
