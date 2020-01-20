import pytest

from game.engine import Deck, Game

def test_deck():
    deck = Deck()
    assert len(deck.cards) == 52

def test_deck_draw():
    deck = Deck()
    assert deck.draw().rank in list(range(2, 15))
    assert deck.draw().suit in ['h', 'd', 'c', 's']

def test_game():
    game = Game(players=2)
    assert len(game.players)

def test_player():
    game = Game(players=2)
    second_player = game.players[1]
    assert second_player.stack == 100

def test_game_has_deck():
    game = Game(players=2)
    deck = game.deck
    assert len(deck.cards)

def test_game_can_deal_cards():
    game = Game(players=2)
    game.deal()
    assert len(game.deck) == 48
    assert len(game.players[0].hole_cards) == 2
    assert len(game.players[1].hole_cards) == 2