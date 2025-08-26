from Inventory import Inventory
from CardDeck import CardDeck
from Move import Move
import random
from copy import deepcopy

class GameState:
    players: list[Inventory]
    initial_player: int
    turnPlayer: int
    deck: CardDeck
    current_sequence: list[Move]
    score: list[int]
    number_of_players: int

    def __init__(self, number_of_players: int = 2) -> None:
        self.number_of_players = number_of_players
        self.score = [0] * number_of_players
        self.reset()

    def reset(self) -> None:
        self.players = [Inventory() for _ in range(self.number_of_players)]
        self.initial_player = random.randint(0, self.number_of_players - 1)
        self.turnPlayer = self.initial_player
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
    number_of_players: int

    def __init__(self, gameState: GameState, playerId: int) -> None:
        self.player = deepcopy(gameState.players[playerId])
        self.playerId = deepcopy(playerId)
        self.initial_player = deepcopy(gameState.initial_player)
        self.current_sequence = deepcopy(gameState.current_sequence)
        self.score = deepcopy(gameState.score)
        self.number_of_players = deepcopy(gameState.number_of_players)
        self.players_card_num = [len(inv.cards) for inv in gameState.players]
        self.players_money = [inv.money for inv in gameState.players]

    def __str__(self) -> str:
        return f"""GAME STATE
        You're {self.playerId + 1} player out of {self.number_of_players}
        Your hand {self.player}
        Sequence {self.current_sequence} started by {self.initial_player + 1}
        Players card numbers {self.players_card_num}, players money {self.players_money}
        Current score {self.score}"""
