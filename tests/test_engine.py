import numpy as np

from game.engine import Card, Deck, Game
from game.engine import is_straight, is_flush, is_straight_flush, is_quads


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


def test_is_straight_not():
    hand = [14, 12, 10, 9, 8, 6, 2]
    hand = [Card(rank, "h") for rank in hand]
    assert not is_straight(hand)


def test_is_straight_various():
    situations = [
        ([14, 13, 12, 11, 10, 3, 2], True),
        ([6, 6, 5, 5, 4, 3, 2], True),
        ([14, 13, 12, 5, 4, 3, 2], True),
        ([14, 13, 10, 7, 4, 3, 2], False),
    ]

    def ranks_to_hand(ranks):
        return [Card(rank, "h") for rank in ranks]

    situations = [
        (ranks_to_hand(situation), outcome) for situation, outcome in situations
    ]

    test_outcomes = np.asarray(
        [bool(is_straight(hand)) == true_outcome for hand, true_outcome in situations]
    )
    assert test_outcomes.all()


def test_is_flush_various():
    situations = [
        (
            [
                Card(10, "h"),
                Card(10, "h"),
                Card(9, "h"),
                Card(5, "h"),
                Card(9, "h"),
                Card(4, "s"),
                Card(2, "s"),
            ],
            10,
        ),
        (
            [
                Card(10, "h"),
                Card(10, "h"),
                Card(9, "h"),
                Card(5, "h"),
                Card(9, "s"),
                Card(4, "s"),
                Card(2, "s"),
            ],
            False,
        ),
    ]

    test_outcomes = [is_flush(hand) == outcome for hand, outcome in situations]
    assert all(test_outcomes)


def test_is_straight_flush():
    situations = [
        (
            [
                Card(14, "s"),
                Card(13, "h"),
                Card(12, "h"),
                Card(11, "h"),
                Card(10, "h"),
                Card(4, "h"),
                Card(2, "h"),
            ],
            False,
        ),
        (
            [
                Card(14, "h"),
                Card(13, "h"),
                Card(12, "h"),
                Card(11, "h"),
                Card(10, "h"),
                Card(4, "s"),
                Card(2, "s"),
            ],
            14,
        ),
    ]
    test_outcomes = [is_straight_flush(hand) == outcome for hand, outcome in situations]
    assert all(test_outcomes)


def test_is_quads():
    situations = [
        (
            [
                Card(14, "s"),
                Card(14, "h"),
                Card(14, "d"),
                Card(14, "c"),
                Card(10, "h"),
                Card(4, "h"),
                Card(10, "h"),
            ],
            (14, 10),
        ),
        (
            [
                Card(14, "s"),
                Card(13, "h"),
                Card(14, "d"),
                Card(14, "c"),
                Card(10, "h"),
                Card(4, "h"),
                Card(2, "h"),
            ],
            False,
        ),
    ]
    test_outcomes = [is_quads(hand) == outcome for hand, outcome in situations]
    assert all(test_outcomes)
