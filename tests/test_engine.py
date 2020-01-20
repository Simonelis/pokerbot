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

def test_big_blinds_and_button_and_pot():
    game = Game(players=4, button_position=2)
    game.deal()
    game.post_blinds()

    assert game.pot == 1.5
    assert game.players[0].stack == 99
    assert game.players[1].stack == 100
    assert game.players[2].stack == 100
    assert game.players[3].stack == 99.5
    