from .Inventory import Inventory
from .CardDeck import CardDeck
from .Move import Move
import random
from copy import deepcopy

class GameState:
    players: list[Inventory]
    initial_player: int
    turn_player: int
    deck: CardDeck
    current_sequence: list[Move]
    score: list[int]

    def __init__(self) -> None:
        self.score = [0, 0]
        self.reset()

    def reset(self) -> None:
        self.players = [Inventory(), Inventory()]
        self.initial_player = random.randint(0, 1)
        self.turn_player = self.initial_player
        self.deck = CardDeck()
        self.current_sequence = []

class PlayerInfo:
    player: Inventory
    playerId: int
    players_card_num: list[int]
    players_money: list[int]
    initial_player: int
    current_sequence: list[Move]
    score: list[int]

    def __init__(self, gameState: GameState, playerId: int) -> None:
        self.player = deepcopy(gameState.players[playerId])
        self.playerId = deepcopy(playerId)
        self.initial_player = deepcopy(gameState.initial_player)
        self.current_sequence = deepcopy(gameState.current_sequence)
        self.score = deepcopy(gameState.score)
        self.players_card_num = [len(inv.cards) for inv in gameState.players]
        self.players_money = [inv.money for inv in gameState.players]

    def __str__(self) -> str:
        return f"""GAME STATE
        You're {self.playerId + 1}
        Your hand {self.player}
        Sequence {self.current_sequence} started by {self.initial_player + 1}
        Players card numbers {self.players_card_num}, players money {self.players_money}
        Current score {self.score}"""
