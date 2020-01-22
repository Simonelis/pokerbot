import pytest

from game.engine import Card, Deck, Game
from game.engine import is_straight


def test_deck():
    deck = Deck()
    assert len(deck.cards) == 52


def test_deck_draw():
    deck = Deck()
    assert deck.draw().rank in list(range(2, 15))
    assert deck.draw().suit in ["h", "d", "c", "s"]


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


def test_flop():
    game = Game(players=2)
    game.deal()
    game.flop()
    assert len(game.board) == 3


def test_turn():
    game = Game(players=2)
    game.deal()
    game.flop()
    game.turn()
    assert len(game.board) == 4
    assert len(game.deck.cards) == 44


def test_river():
    game = Game(players=5)
    game.deal()
    game.flop()
    game.turn()
    game.river()
    assert len(game.board) == 5
    assert len(game.deck.cards) == 37


def test_player_hand_has_right_number_cards():
    game = Game(players=3)

    game.deal()
    hand = game.get_player_hand(player=2)
    assert len(hand) == 2

    game.flop()
    hand = game.get_player_hand(player=2)
    assert len(hand) == 5

    game.turn()
    hand = game.get_player_hand(player=2)
    assert len(hand) == 6

    game.river()
    hand = game.get_player_hand(player=2)
    assert len(hand) == 7


def test_is_straight():
    hand = [14, 13, 12, 11, 10, 9, 8]
    hand = [Card(rank, "h") for rank in hand]
    assert is_straight(hand)
