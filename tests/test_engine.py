import pytest

from game.engine import Deck

def test_deck():
    deck = Deck()
    assert len(deck.cards) == 52

# def test_deck_draw():
#     deck = Deck()
#     assert deck.draw().rank is in list(range(13))