from WorldConflict.CardDeck import CardDeck
from WorldConflict.Card import Card
from collections import Counter
from copy import deepcopy
import pytest

def test_init():
    deck = CardDeck()

    assert Counter(deck.drawPile) == Counter([Card.ACE] * 3 + [Card.KING] * 3 + [Card.QUEEN] * 3 + [Card.JACK] * 3 + [Card.TWO] * 3)

    deck.shuffle()

    assert Counter(deck.drawPile) == Counter([Card.ACE] * 3 + [Card.KING] * 3 + [Card.QUEEN] * 3 + [Card.JACK] * 3 + [Card.TWO] * 3)

def test_draw():
    deck = CardDeck()

    deck.shuffle()
    oldPile = deepcopy(deck.drawPile)

    card1 = deck.draw()
    card2 = deck.draw()

    assert oldPile[-1] == card1
    assert oldPile[-2] == card2
    assert oldPile[:-2] == deck.drawPile

def test_empty():
    deck = CardDeck()

    deck.drawPile = []
    with pytest.raises(RuntimeError):
        deck.draw()

def test_discard():
    deck = CardDeck()

    ret1 = deck.discard(Card.KING)
    ret2 = deck.discard(Card.ANY)

    assert ret1 == False
    assert ret2 == True
    assert deck.discardPile == [Card.KING]
