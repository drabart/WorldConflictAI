from WorldConflict.Game import Game, take_move
from WorldConflict.Move import Move
from WorldConflict.Card import Card
from WorldConflict.IAgent import IAgent
from WorldConflict.GameState import GameState, PlayerInfo
from WorldConflict.Inventory import Inventory
from WorldConflict.CardDeck import CardDeck

from unittest.mock import Mock
from collections import Counter

class MockAgent(IAgent):
    move_order: list[Move]
    card_discard_order: list[Card]

    def __init__(self, move_order: list[Move], card_discard_order: list[Card]) -> None:
        super().__init__()
        self.move_order = move_order
        self.card_discard_order = card_discard_order

    def generate_give_card(self, state: PlayerInfo, card_preference: Card) -> Card:
        card = self.card_discard_order[0]
        self.card_discard_order = self.card_discard_order[1:]
        return card
    
    def generate_move(self, state: PlayerInfo) -> Move:
        card = self.move_order[0]
        self.move_order = self.move_order[1:]
        return card
    
def test_ace_ok():
    agent1 = MockAgent([Move.PLAY_ACE], [Card.ACE, Card.JACK, Card.TWO])
    agent2 = MockAgent([Move.OK], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.JACK, Card.JACK, Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.ACE)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 2
    assert Counter(player1_inventory.cards) == Counter([Card.ACE, Card.JACK])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert Counter(game_state.deck.drawPile) == Counter([])
    assert game_state.deck.discardPile == [Card.ACE, Card.JACK, Card.TWO]

def test_king_ok():
    agent1 = MockAgent([Move.PLAY_KING], [Card.KING])
    agent2 = MockAgent([Move.OK], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.ACE]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.KING)
    player1_inventory.cards.append(Card.KING)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 5
    assert Counter(player1_inventory.cards) == Counter([Card.ACE, Card.KING])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.KING]

def test_jack_ok():
    agent1 = MockAgent([Move.PLAY_JACK], [Card.JACK])
    agent2 = MockAgent([Move.OK], [Card.QUEEN])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.KING]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.JACK)
    player1_inventory.cards.append(Card.ACE)
    player1_inventory.money = 3
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 0
    assert Counter(player1_inventory.cards) == Counter([Card.ACE, Card.KING])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert Counter(game_state.deck.drawPile) == Counter([])
    assert game_state.deck.discardPile == [Card.JACK, Card.QUEEN]

def test_two_ok():
    agent1 = MockAgent([Move.PLAY_TWO], [Card.TWO])
    agent2 = MockAgent([Move.OK], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.KING]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.TWO)
    player1_inventory.cards.append(Card.ACE)
    player1_inventory.money = 3
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 5
    assert Counter(player1_inventory.cards) == Counter([Card.KING, Card.ACE])

    assert player2_inventory.money == 0
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert Counter(game_state.deck.drawPile) == Counter([])
    assert game_state.deck.discardPile == [Card.TWO]

def test_plus_one_ok():
    agent1 = MockAgent([Move.PLAY_PLUS_ONE], [])
    agent2 = MockAgent([Move.OK], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = []

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.KING)
    player1_inventory.cards.append(Card.KING)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 3
    assert Counter(player1_inventory.cards) == Counter([Card.KING, Card.KING])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == []

def test_plus_two_ok():
    agent1 = MockAgent([Move.PLAY_PLUS_TWO], [])
    agent2 = MockAgent([Move.OK], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = []

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.KING)
    player1_inventory.cards.append(Card.KING)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 4
    assert Counter(player1_inventory.cards) == Counter([Card.KING, Card.KING])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == []

def test_affair_ok():
    agent1 = MockAgent([Move.PLAY_AFFAIR], [])
    agent2 = MockAgent([Move.OK], [Card.QUEEN])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = []

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.KING)
    player1_inventory.cards.append(Card.KING)
    player1_inventory.money = 7
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 0
    assert Counter(player1_inventory.cards) == Counter([Card.KING, Card.KING])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert Counter(game_state.deck.discardPile) == Counter([Card.QUEEN])

def test_bluff_called_one_success():
    agent1 = MockAgent([Move.PLAY_KING], [Card.JACK])
    agent2 = MockAgent([Move.CALL_BLUFF], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = []

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.JACK)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 2
    assert Counter(player1_inventory.cards) == Counter([Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.JACK]

def test_bluff_called_one_fail():
    agent1 = MockAgent([Move.PLAY_KING], [Card.KING])
    agent2 = MockAgent([Move.CALL_BLUFF], [Card.QUEEN])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.KING)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 5
    assert Counter(player1_inventory.cards) == Counter([Card.TWO, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.KING, Card.QUEEN]

def test_bounds_checked():
    agent1 = MockAgent([Move.PLAY_JACK, Move.PLAY_JACK, Move.PLAY_AFFAIR, Move.PLAY_AFFAIR], [])
    agent2 = MockAgent([], [])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = []

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.JACK)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.QUEEN)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    move = take_move(game_state, player1_inventory, agent1)
    assert move == Move.FORFEIT

    player1_inventory.money = 3
    move = take_move(game_state, player1_inventory, agent1)
    assert move == Move.PLAY_JACK

    player1_inventory.money = 6
    move = take_move(game_state, player1_inventory, agent1)
    assert move == Move.FORFEIT

    player1_inventory.money = 7
    move = take_move(game_state, player1_inventory, agent1)
    assert move == Move.PLAY_AFFAIR

def test_block_plus_two_with_king():
    agent1 = MockAgent([Move.PLAY_PLUS_TWO, Move.OK], [])
    agent2 = MockAgent([Move.BLOCK_PLUS_TWO_WITH_KING], [Card.KING])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.ACE)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.KING)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 2
    assert Counter(player1_inventory.cards) == Counter([Card.ACE, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.QUEEN, Card.TWO])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.KING]

def test_block_jack_with_queen():
    agent1 = MockAgent([Move.PLAY_JACK, Move.OK], [Card.JACK])
    agent2 = MockAgent([Move.BLOCK_JACK_WITH_QUEEN], [Card.QUEEN])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.ACE, Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.JACK)
    player1_inventory.cards.append(Card.ACE)
    player1_inventory.money = 4
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.KING)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 4
    assert Counter(player1_inventory.cards) == Counter([Card.TWO, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.ACE, Card.KING])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.JACK, Card.QUEEN]

def test_block_two_with_two():
    agent1 = MockAgent([Move.PLAY_TWO, Move.OK], [Card.TWO])
    agent2 = MockAgent([Move.BLOCK_TWO_WITH_TWO], [Card.TWO])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.ACE, Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.TWO)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.KING)
    player2_inventory.cards.append(Card.TWO)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 2
    assert Counter(player1_inventory.cards) == Counter([Card.TWO, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.ACE, Card.KING])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.TWO, Card.TWO]

def test_block_two_with_ace():
    agent1 = MockAgent([Move.PLAY_TWO, Move.OK], [Card.TWO])
    agent2 = MockAgent([Move.BLOCK_TWO_WITH_ACE], [Card.ACE])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.ACE, Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.TWO)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.KING)
    player2_inventory.cards.append(Card.ACE)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 2
    assert Counter(player1_inventory.cards) == Counter([Card.TWO, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.ACE, Card.KING])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.TWO, Card.ACE]

def test_bluff_not_checked():
    agent1 = MockAgent([Move.PLAY_TWO, Move.OK], [Card.JACK])
    agent2 = MockAgent([Move.BLOCK_TWO_WITH_TWO], [Card.QUEEN])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.ACE, Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.JACK)
    player1_inventory.cards.append(Card.ACE)
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.KING)
    player2_inventory.cards.append(Card.QUEEN)

    game_state.players = [player1_inventory, player2_inventory]
    game.game_state = game_state

    game.process_game_step()
    game.process_game_step()
    game.process_game_step()

    assert player1_inventory.money == 2
    assert Counter(player1_inventory.cards) == Counter([Card.TWO, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([Card.ACE, Card.KING])

    assert game_state.initial_player == 1
    assert game_state.turn_player == 1

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.JACK, Card.QUEEN]

def test_call_bluff_on_second():
    agent1 = MockAgent([Move.PLAY_JACK, Move.CALL_BLUFF], [Card.JACK])
    agent2 = MockAgent([Move.BLOCK_JACK_WITH_QUEEN], [Card.TWO, Card.KING])
    
    game = Game([agent1, agent2])
    game_state = GameState()

    deck = CardDeck()
    deck.drawPile = [Card.TWO]

    game_state.deck = deck
    game_state.initial_player = 0
    game_state.turn_player = 0

    player1_inventory = Inventory()
    player1_inventory.cards.append(Card.JACK)
    player1_inventory.cards.append(Card.ACE)
    player1_inventory.money = 4
    player2_inventory = Inventory()
    player2_inventory.cards.append(Card.KING)
    player2_inventory.cards.append(Card.TWO)

    game_state.players = [player1_inventory, player2_inventory]

    game.game_state = game_state
    game_state.reset = Mock()

    game.process_game_step()
    game.process_game_step()
    game.process_game_step()

    game_state.reset.assert_called_once()

    assert player1_inventory.money == 1
    assert Counter(player1_inventory.cards) == Counter([Card.TWO, Card.ACE])

    assert player2_inventory.money == 2
    assert Counter(player2_inventory.cards) == Counter([])

    assert game_state.deck.drawPile == []
    assert game_state.deck.discardPile == [Card.JACK, Card.TWO, Card.KING]

    assert game_state.score == [1, 0]
